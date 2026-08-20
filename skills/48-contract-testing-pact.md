# Skill 48: Contract Testing (Pact)

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 48. Contract Testing (Pact)

Contract tests verify that service boundaries are respected — that providers meet consumer expectations and consumers don't depend on undocumented behavior.

### 48.1 Consumer-Driven Contract Testing

A **consumer** defines what it expects from a **provider**. The provider verifies it meets all consumers' expectations.

```
Consumer A (Web App) ──> expects GET /users/{id} returns {id, name, email}
Consumer B (Mobile)  ──> expects GET /users/{id} returns {id, name, email, avatar_url}
                          ↓
Provider (User API) ───── Must satisfy ALL consumer expectations
```

### 48.2 Setup with Pact (Python)

```bash
pip install pact-python
```

### 48.3 Consumer Test (Defines Expectations)

```python
# tests/contract/consumer/test_user_api_contract.py
import pytest
from pact import Pact

pact = Pact(consumer="WebApp", provider="UserAPI", host_name="localhost", port=1234, pact_dir="./pacts")

def test_get_user():
    """WebApp expects GET /users/{id} to return specific fields."""
    expected_response = {
        "id": 42,
        "name": "Alice Smith",
        "email": "alice@example.com"
    }

    (pact
     .given("a user with id 42 exists")
     .upon_receiving("a request for user 42")
     .with_request("GET", "/users/42")
     .will_respond_with(200, body=expected_response))

    with pact:
        result = UserAPIClient("http://localhost:1234").get_user(42)

    assert result.id == 42
    assert result.name == "Alice Smith"
    assert result.email == "alice@example.com"
    # Note: does NOT assert avatar_url — WebApp doesn't need it
```

### 48.4 Provider Verification (Satisfies Consumer Expectations)

```python
# tests/contract/provider/test_user_api_contract.py
import pytest
from pact import Verifier

def test_verify_user_api():
    """Verify the running User API satisfies all consumer contracts."""
    verifier = (
        Verifier(provider="UserAPI", provider_base_url="http://localhost:8000")
        .add_transport("http")
        .set_provider_state("a user with id 42 exists", setup_state)
    )
    verifier.verify_with_broker(
        broker_url="https://pact-broker.example.com",
        broker_token=os.environ["PACT_BROKER_TOKEN"],
        publish_version=os.environ.get("GITHUB_SHA", "dev"),
    )
```

> pact-python v3/v4 API: use `Verifier().add_transport(...).verify_with_broker(...)` or `.verify()` (which raises on failure) — the older `pact-verifier` CLI and `Consumer`/`Provider` classes are deprecated.

```python
# Provider state setup endpoint
@app.post("/_pact/provider_states")
async def provider_states(request: ProviderStateRequest):
    """Set up test state for Pact verification."""
    if request.state == "a user with id 42 exists":
        db.add(User(id=42, name="Alice Smith", email="alice@example.com"))
        db.commit()
        return {"status": "ok"}
    raise ValueError(f"Unknown state: {request.state}")
```

### 48.5 Contract Testing in CI

```yaml
contract-test:
  name: Contract Tests
  runs-on: ubuntu-latest
  services:
    user-api:
      image: user-api:test
      ports:
        - 8000:8000
  steps:
    - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

    - name: Generate consumer contracts
      run: pytest tests/contract/consumer/ -k "consumer"

    - name: Verify provider against contracts
      run: |
        python -m pytest tests/contract/provider/ -k "provider"

    - name: Check if safe to deploy (can-i-deploy)
      run: |
        pact-broker can-i-deploy \
          --pacticipant WebApp \
          --version=${{ github.sha }} \
          --to-environment production \
          --broker-base-url=https://pact-broker.example.com \
          --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
```

### 48.6 What to Contract Test

| Contract Type | When to Use | Example |
|---------------|-------------|---------|
| **API responses** | Always | Verify response schema, fields, types |
| **Error responses** | Always | Verify error format, status codes |
| **HTTP headers** | Often | Content-Type, auth headers |
| **Query parameters** | When used | Filtering, pagination, sorting |
| **Event schemas** | For event-driven | Message format, required fields |
| **Async callbacks** | For webhooks | Callback URL, payload format |

### 48.7 Contract Versioning

```python
# In consumer test, include version
pact = Consumer("WebApp", version="1.2.3").has_pact_with(
    Provider("UserAPI"),
    pact_dir="./pacts"
)

# Pact Broker stores all versions, enables:
# - Backward compatibility checking
# - Can-I-Deploy checks
# - Dependency graph visualization
```

---

