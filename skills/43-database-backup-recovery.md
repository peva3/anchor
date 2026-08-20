# Skill 43: Database Backup & Recovery

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 43. Database Backup & Recovery

Data loss is a resume-generating event. Every project with persistent data MUST implement backup and recovery.

### 43.1 Backup Schedule

| Frequency | Retention | Purpose |
|-----------|-----------|---------|
| **Daily** | 7 days | Point-in-time recovery for recent mistakes |
| **Weekly** | 4 weeks | Extended recovery window for delayed-discovered issues |
| **Monthly** | 12 months | Long-term compliance and audit requirements |

This is the **Grandfather-Father-Son** retention pattern.

### 43.2 PostgreSQL Backup Implementation

```python
import subprocess
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class DatabaseBackup:
    def __init__(
        self,
        db_url: str,
        backup_dir: Path,
        retention_daily: int = 7,
        retention_weekly: int = 4,
        retention_monthly: int = 12
    ):
        self.db_url = db_url
        self.backup_dir = backup_dir
        self.retention_daily = retention_daily
        self.retention_weekly = retention_weekly
        self.retention_monthly = retention_monthly

    def create_backup(self) -> Path:
        """Create a compressed backup of the database."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_path = self.backup_dir / f"backup_{timestamp}.sql"
        gz_path = self.backup_dir / f"backup_{timestamp}.sql.gz"

        try:
            # Dump database
            subprocess.run(
                ["pg_dump", self.db_url, "-f", str(sql_path)],
                check=True,
                capture_output=True,
                timeout=3600  # 1 hour timeout for large databases
            )

            # Compress
            with open(sql_path, "rb") as f_in:
                with gzip.open(gz_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove uncompressed
            sql_path.unlink()

            return gz_path

        except subprocess.TimeoutExpired:
            sql_path.unlink(missing_ok=True)
            raise RuntimeError("Backup timed out after 1 hour")
        except Exception:
            sql_path.unlink(missing_ok=True)
            gz_path.unlink(missing_ok=True)
            raise

    def rotate_backups(self):
        """Apply retention policy — delete expired backups."""
        backups = sorted(self.backup_dir.glob("backup_*.sql.gz"))

        now = datetime.now()
        kept_daily = []
        kept_weekly = []
        kept_monthly = []

        for backup_path in backups:
            try:
                backup_date = datetime.strptime(
                    backup_path.name, "backup_%Y%m%d_%H%M%S.sql.gz"
                )
            except ValueError:
                continue

            age_days = (now - backup_date).days

            if age_days <= self.retention_daily:
                kept_daily.append(backup_path)
                continue

            if age_days <= self.retention_weekly * 7:
                # Keep one per week (Monday)
                if backup_date.weekday() == 0:
                    kept_weekly.append(backup_path)
                    continue

            if age_days <= self.retention_monthly * 30:
                # Keep one per month (1st of month)
                if backup_date.day == 1:
                    kept_monthly.append(backup_path)
                    continue

            # Expired — delete
            backup_path.unlink()

    def list_backups(self) -> list[dict]:
        """List available backups with metadata."""
        backups = sorted(self.backup_dir.glob("backup_*.sql.gz"), reverse=True)
        return [
            {
                "filename": p.name,
                "size_bytes": p.stat().st_size,
                "size_mb": round(p.stat().st_size / (1024 * 1024), 2),
                "timestamp": datetime.strptime(
                    p.name, "backup_%Y%m%d_%H%M%S.sql.gz"
                ).isoformat()
            }
            for p in backups
        ]
```

### 43.3 Restore Procedure

```bash
# 1. Stop application (prevent writes during restore)
docker compose stop app

# 2. Drop existing database (CAUTION — data loss)
docker compose exec postgres dropdb -U postgres mydb

# 3. Create fresh database
docker compose exec postgres createdb -U postgres mydb

# 4. Restore from backup
gunzip -c /backups/backup_20260615_120000.sql.gz | \
    docker compose exec -T postgres psql -U postgres mydb

# 5. Start application
docker compose start app

# 6. Verify restore
curl -f http://localhost:8000/health
```

### 43.4 Backup Verification

Automated restore test — validates backup integrity:

```python
def verify_backup(backup_path: Path, test_db_url: str) -> bool:
    """Restore backup to ephemeral test database and verify."""
    try:
        # Restore to test database
        subprocess.run(
            f"gunzip -c {backup_path} | psql {test_db_url}",
            shell=True, check=True, capture_output=True, timeout=600
        )

        # Verify critical tables exist and have data
        result = subprocess.run(
            f"psql {test_db_url} -c \"SELECT count(*) FROM information_schema.tables WHERE table_schema='public'\"",
            shell=True, check=True, capture_output=True, text=True
        )

        table_count = int(result.stdout.strip().split('\n')[-2].strip())
        return table_count > 0

    except Exception as e:
        logger.error("Backup verification failed for %s: %s", backup_path.name, e)
        return False
    finally:
        # Clean up test database
        subprocess.run(
            f"psql {test_db_url} -c \"DROP SCHEMA public CASCADE; CREATE SCHEMA public\"",
            shell=True, capture_output=True
        )
```

### 43.5 Backup Monitoring

Alert if:
- **Backup failed** — No successful backup in past 25 hours
- **Backup size anomaly** — Today's backup is <50% or >200% of average
- **Verification failed** — Latest backup failed verification test
- **Off-site sync failed** — S3/GCS replication error
- **Retention violation** — More backups than configured retention policy allows

### 43.6 Off-Site Backup Replication

```bash
# Sync backups to S3 (run after each backup)
aws s3 sync /var/backups/ s3://mycompany-backups/myproject/ \
    --storage-class STANDARD_IA \
    --sse AES256

# Verify sync
aws s3 ls s3://mycompany-backups/myproject/ --recursive | wc -l
```

---

