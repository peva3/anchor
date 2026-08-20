# Skill 44: Secrets Management

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 44. Secrets Management

Secrets in code is the #2 cause of security incidents (after phishing). Every project MUST use a tiered secrets strategy.

### 44.1 Tiered Secrets Strategy

| Tier | Tool | When to Use | Security Level |
|------|------|-------------|----------------|
| **Local Development** | `.env` files (never committed) | Individual developers | Low — single developer |
| **Team Development** | Doppler / 1Password CLI | Small teams, shared secrets | Medium — access controlled |
| **CI/CD** | GitHub Secrets / GitLab CI Variables | Build pipeline secrets | Medium — scoped to repo |
| **GitOps** | SOPS + Age/PGP | Encrypted secrets in git, decrypted at deploy | High — encrypted at rest |
| **Cloud-Native** | AWS Secrets Manager / Azure Key Vault / GCP Secret Manager | Cloud provider managed, IAM-integrated | High — managed rotation |
| **Enterprise** | HashiCorp Vault | Dynamic secrets, leasing, audit logging, PKI | Highest — full audit trail |

### 44.2 SOPS + Age Encryption (GitOps Pattern)

```bash
# Install SOPS and age
brew install sops age

# Generate age key
age-keygen -o ~/.config/sops/age/keys.txt

# Create .sops.yaml configuration
cat > .sops.yaml << 'EOF'
creation_rules:
  - path_regex: secrets/dev\.yaml$
    age: >-
      age1abc123...
  - path_regex: secrets/prod\.yaml$
    age: >-
      age1xyz789...
EOF

# Encrypt secrets file
sops --encrypt secrets.yaml > secrets.enc.yaml

# Edit encrypted file
sops secrets.enc.yaml

# Decrypt at deploy time
sops --decrypt secrets.enc.yaml > secrets.yaml
```

### 44.3 Secrets That MUST Be Managed

| Secret Type | Storage | Rotation | Justification |
|------------|---------|----------|---------------|
| **Database passwords** | Vault / Secrets Manager | 90 days | Primary data access |
| **API keys (third-party)** | Vault / Secrets Manager | 90 days | External service access |
| **Encryption keys** | Vault / KMS | 365 days | Data encryption at rest |
| **JWT signing secrets** | Vault / Secrets Manager | 90 days | Auth token integrity |
| **TLS certificates** | Cert Manager / ACM | Auto-renew | HTTPS termination |
| **OAuth client secrets** | Vault / Secrets Manager | 180 days | Third-party auth |
| **Webhook secrets** | Vault / Secrets Manager | 90 days | Inbound verification |
| **CI/CD deploy tokens** | GitHub Secrets / Vault | 90 days | Deployment pipeline |

### 44.4 Secret Rotation Pattern

```python
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import base64

class SecretRotator:
    def __init__(self, vault_client, key_path: str, rotation_days: int = 90):
        self.vault = vault_client
        self.key_path = key_path
        self.rotation_days = rotation_days

    def needs_rotation(self) -> bool:
        """Check if secret is due for rotation."""
        metadata = self.vault.read_metadata(self.key_path)
        created = datetime.fromisoformat(metadata["created_time"])
        age_days = (datetime.now() - created).days
        return age_days >= self.rotation_days

    def rotate(self) -> None:
        """Rotate a secret with zero-downtime dual-key window."""
        # 1. Generate new secret
        new_key = base64.urlsafe_b64encode(Fernet.generate_key()).decode()
        old_key = self.vault.read_secret(self.key_path)["value"]

        # 2. Store new key alongside old (dual-key window)
        self.vault.write_secret(f"{self.key_path}_new", {"value": new_key})

        # 3. Deploy new key to all services
        self._deploy_key(new_key)

        # 4. Promote new key to primary
        self.vault.write_secret(self.key_path, {"value": new_key, "previous": old_key})

        # 5. Remove temporary key
        self.vault.delete_secret(f"{self.key_path}_new")

        # 6. Monitor for old-key failures (grace period)
        # After grace period, old key is no longer valid

    def _deploy_key(self, key: str) -> None:
        """Deploy new key to all services."""
        # Trigger config reload on all instances
        # Implementation depends on deployment architecture
        pass
```

### 44.5 Secret Scanning in CI

```yaml
# Add to ci.yml
- name: Scan for secrets
  uses: gitleaks/gitleaks-action@v2
  with:
    config-path: .gitleaks.toml
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# Or with truffleHog
- name: Scan for secrets
  run: |
    pip install trufflehog3
    trufflehog3 --format json --output trufflehog-report.json .
```

### 44.6 Secrets Management Rules

- **NEVER** commit secrets to git — enforced by pre-commit `detect-secrets` and CI scanning
- **NEVER** share secrets via email, Slack, or any unencrypted channel
- **NEVER** hardcode secrets in Docker images — use runtime injection
- **NEVER** log secrets — implement PII redaction (Section 41.5)
- **ALWAYS** use a secrets manager (not `.env` files) for production
- **ALWAYS** rotate secrets on a schedule — automate rotation
- **ALWAYS** use least privilege — each service gets only the secrets it needs
- **ALWAYS** use ephemeral credentials when possible (Vault dynamic secrets, OIDC tokens)
- **ALWAYS** audit secret access — who accessed, when, from where
- **NEVER** reuse secrets across environments — dev and prod must have different credentials

---

