# Skill 31: Production Security Patterns

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 31. Production Security Patterns

Hardening patterns for production deployments.

### 31.1 Prompt Injection Detection

Heuristic detection for common prompt injection patterns.

```python
import re
from typing import List

class PromptInjectionDetector:
    PRE_FILTER_PATTERNS = [
        r"system\s*:", r"system\s*-", r"\[INST\]",
        r"<\|im_start\|>", r"<\|im_end\|>", r"\\[system\\]",
    ]

    INJECTION_PATTERNS = [
        (r"(?i)(ignore\s+(previous|all|above)\s+(instructions?|rules?|prompt))", "system_prompt_override"),
        (r"(?i)(you\s+are\s+a\s+dan|do\s+anything\s+now|jailbreak)", "persona_hijack"),
        (r"<\|im_start\|>", "token_injection"),
        (r"(?i)(ignore.*routing|override.*model)", "routing_manipulation"),
        (r"(base64|decode|exec|eval).*['\"]", "encoding_bypass"),
        (r"<!--.*-->", "hidden_comment"),
    ]

    def __init__(self):
        self.pre_filter = re.compile("|".join(self.PRE_FILTER_PATTERNS), re.IGNORECASE)

    def check(self, text: str) -> dict:
        threats = []
        if not self.pre_filter.search(text):
            return {"is_suspicious": False, "threats": [], "threat_level": "NONE"}

        for pattern, name in self.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                threats.append(name)

        return {
            "is_suspicious": len(threats) > 0,
            "threats": threats,
            "threat_level": self._calculate_threat_level(threats)
        }

    def _calculate_threat_level(self, threats: List[str]) -> str:
        if not threats:
            return "NONE"
        elif len(threats) == 1 and threats[0] in ["token_injection", "hidden_comment"]:
            return "LOW"
        elif len(threats) <= 2:
            return "MEDIUM"
        return "HIGH"
```

### 31.2 Admin Audit Logging

Track all admin actions for security and compliance.

```python
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AdminAuditLog(BaseModel):
    id: int
    admin_user_id: int
    action: str
    target_type: str
    target_id: Optional[str]
    changes: dict
    ip_address: str
    user_agent: str
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None

class AuditLogger:
    def log(
        self, admin_user_id: int, action: str, target_type: str,
        target_id: str | None, changes: dict, request: Request,
        success: bool = True, error: str | None = None
    ):
        entry = AdminAuditLog(
            id=None, admin_user_id=admin_user_id, action=action,
            target_type=target_type, target_id=target_id, changes=changes,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
            timestamp=datetime.now(), success=success, error_message=error
        )
        self.db.add(entry)
        self.db.commit()
```

### 31.3 API Key Encryption

Encrypt sensitive keys at rest using Fernet.

```python
from cryptography.fernet import Fernet

class KeyEncryptor:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)

    @classmethod
    def generate_key(cls) -> bytes:
        return Fernet.generate_key()

    def encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
```

### 31.4 Admin IP Whitelist

Restrict admin endpoints to specific IPs.

```python
from fastapi import FastAPI, Request, HTTPException
import ipaddress

class AdminIPWhitelist:
    def __init__(self, allowed_cidrs: list[str]):
        self.networks = [ipaddress.ip_network(cidr) for cidr in allowed_cidrs]

    def is_allowed(self, client_ip: str) -> bool:
        try:
            ip = ipaddress.ip_address(client_ip)
            return any(ip in network for network in self.networks)
        except ValueError:
            return False
```

### 31.5 Security CI/CD Workflow

Weekly vulnerability scanning with auto-issue creation.

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  schedule:
    - cron: '0 8 * * 1'  # Monday 8 AM UTC

jobs:
  vulnerabilities:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pip-audit safety
      - run: pip-audit --format=json --output=pip-audit.json || true
      - run: safety check --json --output=safety.json || true
      - uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            const data = JSON.parse(fs.readFileSync('pip-audit.json', 'utf8'));
            if (data.vulnerabilities?.length > 0) {
              github.rest.issues.create({
                title: 'Security Vulnerabilities Detected',
                body: 'pip-audit found ' + data.vulnerabilities.length + ' vulnerabilities',
                labels: ['security', 'vulnerability']
              });
            }
```

---

