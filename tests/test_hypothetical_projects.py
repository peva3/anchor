"""Hypothetical test projects — simulate how an LLM navigates and applies AGENTS.md rules.

Runs 6 simulated workflows and identifies issues in rule discoverability,
contradictions, guidance gaps, and instruction overload.
"""

import re
import sys
import textwrap
from pathlib import Path
from collections import defaultdict

AGENTS_MD = Path(__file__).resolve().parent.parent / "AGENTS.md"


def load_sections() -> dict[str, str]:
    """Parse AGENTS.md into {section_name: full_text}."""
    text = AGENTS_MD.read_text()
    sections = {}
    current_section = "header"
    current_text: list[str] = []

    for line in text.split("\n"):
        m = re.match(r"^## (\d+\. .+)", line)
        if m:
            if current_text:
                sections[current_section] = "\n".join(current_text)
            current_section = m.group(1)
            current_text = [line]
        else:
            current_text.append(line)
    if current_text:
        sections[current_section] = "\n".join(current_text)

    return sections


def find_sections_by_keyword(sections: dict[str, str], keyword: str) -> list[str]:
    """Find section names containing any of the pipe-separated keywords."""
    return [
        name for name, text in sections.items()
        if re.search(keyword, text, re.IGNORECASE)
    ]


def extract_rules(text: str, pattern: str) -> list[str]:
    """Extract rules matching a pattern (NEVER, MUST, ALWAYS, etc.)."""
    return re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)


# ─── SCENARIO 1: New developer creates first feature ─────────────────────

def test_scenario_1_first_feature(sections):
    """Agent adds a new REST endpoint to an existing FastAPI project."""
    print("=" * 70)
    print("SCENARIO 1: Add a new REST endpoint to existing FastAPI project")
    print("=" * 70)

    # Simulate: agent searches for relevant guidance
    steps = [
        ("Find API design rules", "api design|rest|endpoint"),
        ("Find testing rules", "test|pytest|coverage"),
        ("Find PR rules", "pr size|pull request|branch"),
        ("Find commit rules", "commit message|git workflow"),
        ("Find lint rules", "ruff|vulture|lint|mypy"),
        ("Find review rules", "review|anti-pattern|code quality"),
    ]

    for step_name, keyword in steps:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {step_name}:")
        if matching:
            print(f"    Hit {len(matching)} section(s): {', '.join(matching[:5])}")
        else:
            print(f"    ⚠️  NO matching sections found for '{keyword}'")

    # Check: would the agent find the 800-line PR limit before pushing?
    pr_size_sections = find_sections_by_keyword(sections, "800.line|800 lines")
    print(f"\n  PR size limit search: {len(pr_size_sections)} sections found")
    if not pr_size_sections:
        print("    ❌ ISSUE: Agent would not find PR size limit organically")

    # Check: does the agent know what to actually DO (concrete actions)?
    api_section = sections.get("12. API Design", "")
    has_concrete = "GET" in api_section and "POST" in api_section
    print(f"  API section has concrete HTTP method guidance: {has_concrete}")


# ─── SCENARIO 2: Agent makes a security fix ──────────────────────────────

def test_scenario_2_security_fix(sections):
    """Agent discovers and fixes a SQL injection vulnerability."""
    print("\n" + "=" * 70)
    print("SCENARIO 2: Fix SQL injection vulnerability")
    print("=" * 70)

    # What should the agent do?
    checks = [
        ("Find injection prevention", "sql injection|parameterized|injection"),
        ("Find security section", "security best practices|input validation"),
        ("Find secret scanning rules", "secret|detect-secret|gitleaks"),
        ("Find audit logging rules", "audit log|audit trail"),
        ("Find NEVER list (eval/exec)", "eval.*exec|NEVER.*eval"),
    ]

    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {check_name}:")
        if matching:
            print(f"    ✓ {len(matching)} section(s): {', '.join(matching[:4])}")
        else:
            print(f"    ❌ NO sections found for '{keyword}'")

    # Critical check: does the agent know to scan for similar vulnerabilities?
    audit_keywords = ["similar", "audit", "related", "throughout", "across", "all instances"]
    security_text = "\n".join(
        sections.get(name, "") for name in sections
        if "security" in name.lower() or "injection" in name.lower()
    )
    found_audit = any(kw in security_text.lower() for kw in audit_keywords)
    if not found_audit:
        print("\n  ⚠️  GAP: No guidance to audit for similar vulnerabilities after fixing one")


# ─── SCENARIO 3: Agent reviews a large PR ────────────────────────────────

def test_scenario_3_review_large_pr(sections):
    """Agent reviews a 1,500-line PR that mixes refactoring + features."""
    print("\n" + "=" * 70)
    print("SCENARIO 3: Review a 1,500-line mixed PR (refactor + feature)")
    print("=" * 70)

    # What guidance exists for the reviewer?
    checks = [
        ("PR size violation detection", "800.line|exceed|too large|split"),
        ("Mixed concern detection", "single feature|one concern|mixed"),
        ("Review vocabulary", "over-engineering|review.*tag|delete:|stdlib:|yagni:|shrink:"),
        ("How to reject a PR", "reject|close|request change|split"),
    ]

    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {check_name}:")
        if matching:
            print(f"    ✓ {len(matching)} section(s)")
        else:
            print(f"    ❌ NOT found")

    # Check: does Section 50.5 review vocabulary actually provide rejection criteria?
    review_section = sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    has_review_tags = "delete:" in review_section and "stdlib:" in review_section
    print(f"\n  Review vocabulary has actionable tags: {has_review_tags}")

    # Check: does the agent know what action to take?
    section_33 = sections.get("33. PR & Change Size Standards", "")
    has_split_guidance = "split" in section_33.lower() and "separate" in section_33.lower()
    print(f"  PR size section has split guidance: {has_split_guidance}")


# ─── SCENARIO 4: Agent sets up a brand new project ────────────────────────

def test_scenario_4_new_project(sections):
    """Agent bootstraps a new project from scratch."""
    print("\n" + "=" * 70)
    print("SCENARIO 4: Bootstrap a brand new Python project")
    print("=" * 70)

    # What would the agent need to find?
    steps = [
        ("Find STARTUP.md reference", "STARTUP.md|bootstrap|new project"),
        ("Find project structure", "project structure|src/|tests/|docs/"),
        ("Find gitignore rules", "gitignore|tests/.*ignore"),
        ("Find pre-commit setup", "pre-commit install|pre-commit-config"),
        ("Find CI/CD template", "ci.yml|workflow|github actions"),
        ("Find DEEPDIVE.md template", "DEEPDIVE|deep dive|system narrative"),
        ("Find tech stack guidance", "tech stack|fastapi|next.js|gin"),
    ]

    for step_name, keyword in steps:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {step_name}:")
        if matching:
            print(f"    ✓ {len(matching)} section(s)")
        else:
            print(f"    ❌ NOT found — agent would struggle")


# ─── SCENARIO 5: Agent encounters a flaky test ────────────────────────────

def test_scenario_5_flaky_test(sections):
    """Agent debugs and fixes a test that fails intermittently."""
    print("\n" + "=" * 70)
    print("SCENARIO 5: Fix a flaky test (intermittent CI failure)")
    print("=" * 70)

    # What should the agent do vs what does it do?
    checks = [
        ("Find flaky test section", "flaky|intermittent|non-deterministic"),
        ("Find quarantine mechanism", "quarantine|mark.flaky|rerunfailures"),
        ("Find root cause guidance", "time.sleep|ordering|race condition|isolation"),
        ("Find NEVER guidance (don't delete)", "NEVER.*delete.*flaky|don't delete.*test"),
        ("Find SLA for fix", "7 day|fix.*within|SLA|timer"),
    ]

    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {check_name}:")
        if matching:
            print(f"    ✓ {len(matching)} section(s)")
        else:
            print(f"    ❌ NOT found")


# ─── SCENARIO 6: Agent should refuse to do something ─────────────────────

def test_scenario_6_refuse_action(sections):
    """Agent is asked to create a PR autonomously or enable a paid service."""
    print("\n" + "=" * 70)
    print("SCENARIO 6: Agent asked to create PR without approval / enable paid runner")
    print("=" * 70)

    # The agent should find and apply "never go rogue" and "never spend money"
    checks = [
        ("Never create PR without approval", "never.*PR.*approval|rogue|without.*explicit"),
        ("Never spend money", "spend.*money|cost.*money|billing|paid runner|paid service"),
        ("Never enable billing", "enable.*billing|modify.*billing|change.*plan"),
        ("Always use user identity", "user.*identity|configured.*author|impersonate"),
    ]

    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        print(f"\n  {check_name}:")
        if matching:
            print(f"    ✓ {len(matching)} section(s): {', '.join(matching[:3])}")
        else:
            print(f"    ❌ CRITICAL GAP — agent would NOT refuse this action")

    # Check: are the prohibitions prominent or buried?
    section_2 = sections.get("2. Commit Protocol", "")
    has_rogue = "never go rogue" in section_2.lower()
    has_cost = "never spend money" in section_2.lower()
    print(f"\n  Rogue prohibition in Section 2: {has_rogue}")
    print(f"  Cost prohibition in Section 2: {has_cost}")

    # Check NEVER list
    section_36 = sections.get("36. Explicit Prohibitions — The \"NEVER\" List", "")
    has_cost_never = "financial never" in section_36.lower()
    has_identity_never = "identity never" in section_36.lower()
    print(f"  Financial NEVER subsection exists: {has_cost_never}")
    print(f"  Identity NEVER subsection exists: {has_identity_never}")


# ─── CROSS-CUTTING ANALYSIS ──────────────────────────────────────────────

def test_rule_discoverability(sections):
    """How easy is it to find critical rules without reading the whole doc?"""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: Rule Discoverability Audit")
    print("=" * 70)

    critical_rules = [
        ("PR size limit (800 lines)", "800.*line|800 lines"),
        ("Never spend money", "spend.*money|cost.*money|paid.*service|billing"),
        ("Never go rogue", "never.*rogue|without.*explicit.*approval"),
        ("Lint before commit (ruff+vulture)", "ruff.*vulture|sweep.*before.*commit"),
        ("Coverage floor (80%)", "80%.*coverage|cov-fail-under"),
        ("Decision ladder (YAGNI→minimum)", "decision ladder|yagni.*stdlib"),
        ("Evidence-first (file:line)", "file:line|evidence.*citation"),
        ("Flaky test quarantine", "quarantine|flaky.*mark|rerunfailures"),
        ("Contract testing (Pact)", "pact|contract.*test|consumer.*driven"),
        ("Chaos engineering", "chaos.*engineering|steady.*state|game day"),
    ]

    print(f"\n  {'Rule':<40} {'Sections Found':<20} {'Status':<10}")
    print(f"  {'─'*40} {'─'*20} {'─'*10}")

    issues = []
    for rule_name, keyword in critical_rules:
        matching = find_sections_by_keyword(sections, keyword)
        count = len(matching)
        status = "✓" if count > 0 else "❌ MISSING"
        if count == 0:
            issues.append(rule_name)
        print(f"  {rule_name:<40} {count:<20} {status:<10}")

    if issues:
        print(f"\n  ❌ {len(issues)} rules have zero discoverable sections:")
        for i in issues:
            print(f"     - {i}")


def test_instruction_depth_overload(sections):
    """Check if critical instructions get buried under verbose sections."""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: Instruction Depth & Overload")
    print("=" * 70)

    # Count rules at different document depths
    section_order = list(sections.keys())

    # Rules in first 10 sections vs last 10
    early_sections = section_order[:10]
    late_sections = section_order[-10:]

    # CRITICAL rules: things an agent MUST know in first 500 lines
    critical_in_early = 0
    critical_in_late = 0
    critical_terms = [
        "NEVER", "MUST", "REQUIRED", "CRITICAL", "ALWAYS", "MANDATORY",
        "never go rogue", "never spend", "no dead code", "test-first",
        "commit protocol"
    ]

    for term in critical_terms:
        for name in early_sections:
            if term.lower() in sections[name].lower():
                critical_in_early += 1
                break
        for name in late_sections:
            if term.lower() in sections[name].lower():
                critical_in_late += 1
                break

    print(f"\n  Critical rules in first 10 sections: {critical_in_early}")
    print(f"  Critical rules in last 10 sections: {critical_in_late}")

    if critical_in_late > critical_in_early:
        print("  ⚠️  WARNING: More critical rules are buried late in the document")
        print("     An agent might miss them if it only scans early sections")

    # Check: does the document have a table of contents / section index?
    header_text = sections.get("header", "")
    has_toc = "section" in header_text.lower() and any(
        d in header_text for d in ["1.", "2.", "3."]
    )
    print(f"  Header has section index/TOC: {has_toc}")


def test_contradiction_risk(sections):
    """Look for patterns where rules could conflict when applied together."""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: Contradiction Risk Analysis")
    print("=" * 70)

    risks = []

    # Risk 1: Section 50 says "one line is self-documenting" but Section 27 requires docstrings
    section_50 = sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    section_27 = sections.get("27. Code Quality Standards", "")
    if "one line is self-documenting" in section_50 and "docstring" in section_27:
        risks.append(
            "RISK: Section 50 says 'one line is self-documenting' but Section 27 "
            "requires docstrings on all public APIs. An agent might skip docstring "
            "on a one-line function, violating Section 27."
        )

    # Risk 2: Section 50 says "≤3 lines explanation" but Section 15 requires detailed WHY
    section_15 = sections.get("15. Git Workflow", "")
    if "three short lines" in section_50 and "explain WHY" in section_15:
        risks.append(
            "RISK: Section 50.4 says 'at most three short lines' explanation, but "
            "Section 15 requires detailed WHY-focused commit messages with problem/solution/context. "
            "Agent might truncate commit messages to 3 lines."
        )

    # Risk 3: Section 2 auto-commits, but Section 36 says never without approval
    section_2 = sections.get("2. Commit Protocol", "")
    section_36 = sections.get("36. Explicit Prohibitions — The \"NEVER\" List", "")
    if "automatically commit" in section_2 and "modify billing" in section_36:
        # This is actually NOT a contradiction — auto-commit is allowed, billing is not.
        # But check for clarity
        pass

    # Risk 4: Section 51 says trim to ≤2000 lines but doc itself is 5800 lines
    section_51 = sections.get("51. Instruction Architecture — Context Economy & Self-Improvement", "")
    if "2,000 lines" in section_51:
        risks.append(
            "RISK: Section 51.3 says AGENTS.md should be ≤2,000 lines. The document "
            "itself is ~5,800 lines. The template exception carve-out exists but may "
            "be confusing — an agent might try to 'fix' this by deleting sections."
        )

    for risk in risks:
        print(f"\n  {risk}")
    if not risks:
        print("  No contradiction risks detected")


def test_navigational_holes(sections):
    """Where would an LLM get lost trying to answer specific questions?"""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: Navigational Hole Analysis")
    print("=" * 70)

    # These are things an agent would search for by keyword
    navigational_queries = [
        ("How do I reject a PR?", "reject.*PR|close.*PR|request.*changes"),
        ("How do I split a large PR?", "split.*PR|separate.*PR|stack.*PR"),
        ("What do I do when a test is flaky?", "flaky|intermittent|non-deterministic"),
        ("How do I set up Dependabot?", "dependabot"),
        ("How do I handle a merge conflict?", "merge conflict|conflict.*resolve"),
        ("How do I rollback a bad deployment?", "rollback|revert.*deploy|undo.*deploy"),
        ("How do I rotate secrets?", "rotate.*secret|rotation.*schedule"),
        ("How do I add a new team member?", "onboard|new developer|team member"),
        ("What's the deployment process?", "deploy.*process|deployment.*pipeline|release"),
        ("How do I debug a slow endpoint?", "slow.*endpoint|profile|performance.*debug"),
    ]

    print(f"\n  {'Query':<45} {'Found':<10} {'Sections':<30}")
    print(f"  {'─'*45} {'─'*10} {'─'*30}")

    missing = []
    for query, keyword in navigational_queries:
        matching = find_sections_by_keyword(sections, keyword)
        found = "✓" if matching else "❌"
        if not matching:
            missing.append(query)
        print(f"  {query:<45} {found:<10} {', '.join(matching[:2]):<30}")

    if missing:
        print(f"\n  ❌ {len(missing)} navigational holes — agent cannot find guidance for:")
        for m in missing:
            print(f"     - {m}")


def test_verbosity_burden(sections):
    """How much does an agent have to read to get a simple answer?"""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: Verbosity Burden Analysis")
    print("=" * 70)

    # How many lines to find core rules?
    section_sizes = {name: len(text.split("\n")) for name, text in sections.items()}

    # If an agent only reads the first N sections (common LLM behavior),
    # what does it miss?
    all_names = list(sections.keys())
    first_5 = all_names[2:7]  # Skip header
    last_5 = all_names[-5:]

    first_5_lines = sum(section_sizes.get(n, 0) for n in first_5)
    last_5_lines = sum(section_sizes.get(n, 0) for n in last_5)

    print(f"\n  Lines in first 5 sections: {first_5_lines}")
    print(f"  Lines in last 5 sections: {last_5_lines}")
    print(f"  Ratio (early:late): {first_5_lines / max(last_5_lines, 1):.1f}:1")

    # Check: what % of the total doc are the critical early sections?
    total_lines = sum(section_sizes.values())
    core_sections = ["1. Core Principles", "2. Commit Protocol", "9. Linting & Type Checking"]
    core_lines = sum(section_sizes.get(n, 0) for n in core_sections)
    core_pct = core_lines / total_lines * 100
    print(f"  Core sections (1,2,9) are {core_lines} lines ({core_pct:.1f}% of total)")

    # The LLM might read Section 1 (principles) and think it covers everything
    section_1_lines = section_sizes.get("1. Core Principles", 0)
    section_1_refs = len(re.findall(r"Section \d+", sections.get("1. Core Principles", "")))
    print(f"  Section 1 cross-references to other sections: {section_1_refs}")

    if section_1_refs < 10:
        print(f"  ⚠️  Section 1 has only {section_1_refs} cross-refs — agent may not discover later sections")

    # The document is 5,800 lines. Most LLMs scan, they don't read.
    # Check if there's a condensed summary appendix
    has_condensed = any(
        "condensed" in sections.get(n, "").lower() for n in sections
    )
    print(f"  Has condensed summary appendix: {has_condensed}")


# ─── MAIN ────────────────────────────────────────────────────────────────

# ─── SCENARIO 7: Agent must decide between simplicity and rigor ──────────

def test_scenario_7_simplicity_vs_rigor(sections):
    """Agent is asked to add email validation. Decision ladder says one line (rung 5),
    but security says validate at trust boundaries (Section 50.3). Which wins?"""
    print("\n" + "=" * 70)
    print("SCENARIO 7: Simplicity ladder vs security carve-out (email validation)")
    print("=" * 70)

    # Key question: does the decision ladder (Section 50.1) override security (Section 50.3)?
    section_50 = sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    has_carve_out = "security" in section_50.lower() and "exempt" in section_50.lower()
    print(f"\n  Security carve-out present in Section 50: {has_carve_out}")

    # Does the ladder acknowledge security as a safety carve-out?
    ladder_text = section_50
    security_before_ladder = (
        "input validation" in ladder_text.lower() and
        "safety carve-out" in ladder_text.lower()
    )
    print(f"  Safety carve-outs precede ladder in text: {security_before_ladder}")

    # Check if Section 13 (Security) explicitly covers validation
    section_13 = sections.get("13. Security Best Practices", "")
    has_validation = "input validation" in section_13.lower()
    print(f"  Section 13 covers input validation: {has_validation}")

    # The real issue: an agent might apply the ladder and skip validation
    # because rung 5 (one line) wins over rung 6 (minimum code).
    # Does the safety carve-out PREVENT this?
    has_explicit_override = "do not apply" in ladder_text.lower() or "never be lazy" in ladder_text.lower()
    if not has_explicit_override:
        print("\n  ⚠️  RISK: Agent might apply ladder to security domains.")
        print("     Section 50.3 says security is exempt but the ladder text")
        print("     doesn't explicitly say 'do not apply the ladder to security.'")
        print("     An agent might skip validation because 'one line is self-documenting.'")


# ─── SCENARIO 8: Agent handles conflicts between rules ────────────────────

def test_scenario_8_rule_conflict_resolution(sections):
    """Agent discovers that Section 50.4 says ≤3 lines explanation,
    but Section 15 says commit messages should be detailed with problem/solution/context.
    Which rule does the agent follow, and does the doc tell it which takes precedence?"""
    print("\n" + "=" * 70)
    print("SCENARIO 8: Rule conflict — short commits vs detailed WHY commits")
    print("=" * 70)

    section_50 = sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    section_15 = sections.get("15. Git Workflow", "")

    has_short = "three short lines" in section_50 or "≤3" in section_50
    has_detailed = "problem" in section_15.lower() and "solution" in section_15.lower()

    print(f"\n  Section 50.4 requires short explanations: {has_short}")
    print(f"  Section 15 requires detailed WHY commits: {has_detailed}")

    # Check: does the doc specify which takes priority?
    has_priority_rule = any(
        phrase in (section_50 + section_15).lower()
        for phrase in [
            "takes precedence", "overrides", "applies over",
            "exception", "when in conflict", "priority"
        ]
    )
    print(f"  Document specifies which rule takes priority: {has_priority_rule}")

    if not has_priority_rule:
        print("\n  ⚠️  GAP: No rule conflict resolution mechanism exists.")
        print("     When two sections give conflicting guidance, the agent")
        print("     has no way to determine which takes precedence.")
        print("     Add a meta-rule: 'Specific sections override general ones.'")

    # Check: the cheatsheet tells agent what to do for commits
    all_text = "\n".join(sections.values())
    has_cheatsheet = "Quick-Navigation Cheatsheet" in all_text
    print(f"  Quick-Navigation Cheatsheet exists: {has_cheatsheet}")

    if has_cheatsheet:
        # The cheatsheet entry for commits should point to Section 15, not 50.4
        commit_refs = find_sections_by_keyword(sections, "commit|cheatsheet")
        print(f"  Cheatsheet covers commit guidance: {len(commit_refs) > 0}")


# ─── SCENARIO 9: Agent handles production incident ────────────────────────

def test_scenario_9_production_incident(sections):
    """Database goes down in production. Agent needs to: rollback recent deploy,
    check health endpoints, verify backups, notify team. Is this covered?"""
    print("\n" + "=" * 70)
    print("SCENARIO 9: Production database outage — incident response")
    print("=" * 70)

    checks = [
        ("Rollback procedure", "rollback|revert.*deploy|undo.*deploy"),
        ("Health endpoint check", "health.*endpoint|health.*check|/health"),
        ("Backup verification", "restore.*test|verify.*backup|backup.*verif"),
        ("Incident notification", "notify|alert|on-call|escalat"),
        ("Circuit breaker (prevent cascading)", "circuit.*breaker|half.open"),
        ("Post-mortem process", "post-mortem|after.*action|game day|incident.*review"),
    ]

    covered = 0
    missing = []
    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        if matching:
            covered += 1
            print(f"\n  ✓ {check_name}: {matching[0]}")
        else:
            missing.append(check_name)
            print(f"\n  ❌ {check_name}: NOT FOUND")

    if missing:
        print(f"\n  ⚠️  {len(missing)}/6 incident response areas NOT covered:")
        for m in missing:
            print(f"     - {m}")

    # Check: quick-navigation cheatsheet should have "rollback" entry
    all_text = "\n".join(sections.values())
    has_rollback_cheatsheet = "Rollback a bad deployment" in all_text
    print(f"\n  Cheatsheet has rollback entry: {has_rollback_cheatsheet}")


# ─── SCENARIO 10: Agent builds a multi-service system ─────────────────────

def test_scenario_10_multi_service_system(sections):
    """Agent is building a system with 3 microservices (API, worker, frontend).
    Needs: contract tests between services, CI for each, Docker compose for dev,
    health checks for all 3, observability across the system."""
    print("\n" + "=" * 70)
    print("SCENARIO 10: Build 3-microservice system from scratch")
    print("=" * 70)

    checks = [
        ("Contract testing (Pact)", "pact|contract.*test|consumer.*driven"),
        ("Docker Compose multi-service", "docker.compose|compose.yml|service:"),
        ("Health checks per service", "health.*endpoint|/health|healthcheck"),
        ("Observability across services", "opentelemetry|distributed.*trac|correlation.*id"),
        ("CI for each service", "ci.yml|workflow|matrix"),
        ("Multi-agent coordination", "multi.agent|parallel.*agent|sequential.*handoff"),
        ("Database per service or shared", "database.*per.*service|shared.*database"),
    ]

    covered = 0
    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        if matching:
            covered += 1
        else:
            print(f"\n  ❌ {check_name}: No section covers this")

    pct = covered / len(checks) * 100
    print(f"\n  Multi-service coverage: {covered}/{len(checks)} ({pct:.0f}%)")

    # Specific gaps
    db_per_service = find_sections_by_keyword(sections, "database.*per.*service|shared.*database|one.*database.*per")
    if not db_per_service:
        print("\n  ⚠️  GAP: No guidance on database-per-service vs shared database pattern")


# ─── SCENARIO 11: Agent encounters untested legacy code ────────────────────

def test_scenario_11_legacy_code(sections):
    """Agent is asked to add a feature to a 5-year-old codebase with no tests,
    no linting config, no CI, and no AGENTS.md. What's the playbook?"""
    print("\n" + "=" * 70)
    print("SCENARIO 11: Add feature to legacy codebase (no tests, no CI, no lint)")
    print("=" * 70)

    checks = [
        ("Start with tests before touching code", "test.*before|test-first|write.*test.*before"),
        ("Set up linting first", "pre-commit.*install|pre-commit-config"),
        ("Set up CI first", "ci.yml|workflow|github.*actions"),
        ("Small PR (800-line gate)", "800.line|under.*800|pr.*size"),
        ("Don't refactor + feature in same PR", "single.*feature|one.*concern|don't.*mix"),
        ("Tradeoff comments for shortcuts", "ponytail:|tradeoff.*comment|named.*ceiling"),
    ]

    covered = 0
    for check_name, keyword in checks:
        matching = find_sections_by_keyword(sections, keyword)
        if matching:
            covered += 1
        else:
            print(f"\n  ❌ {check_name}: NOT FOUND")

    pct = covered / len(checks) * 100
    print(f"\n  Legacy codebase coverage: {covered}/{len(checks)} ({pct:.0f}%)")

    # Check: does Section 33.3 prevent the common "while I'm here" refactor?
    section_33 = sections.get("33. PR & Change Size Standards", "")
    has_no_mix = "Do NOT mix" in section_33 or "do not mix" in section_33.lower()
    print(f"  Explicit 'do not mix refactor + feature' rule: {has_no_mix}")


# ─── SCENARIO 12: Agent must handle model-appropriate instruction level ────

def test_scenario_12_model_capability(sections):
    """Agent is running on a small local model (3B params, 8K context).
    It needs the COMPACT tier of instructions, not the FULL tier."""
    print("\n" + "=" * 70)
    print("SCENARIO 12: Small local model needs COMPACT instruction tier")
    print("=" * 70)

    section_51 = sections.get("51. Instruction Architecture — Context Economy & Self-Improvement", "")

    has_tiers = "FULL" in section_51 and "COMPACT" in section_51
    print(f"\n  Tiered detail levels defined: {has_tiers}")

    has_table = "FULL" in section_51 and "STANDARD" in section_51
    print(f"  Tier comparison table present: {has_table}")

    has_condensed = "condensed" in section_51.lower() and "appendix" in section_51.lower()
    print(f"  Condensed appendix for compact contexts: {has_condensed}")

    # Critical: does the doc tell the agent HOW to get to the compact tier?
    has_how = "strip" in section_51.lower() or "reduce" in section_51.lower()
    print(f"  Instructions for reducing to compact: {has_how}")

    if not has_condensed:
        print("\n  ⚠️  GAP: No condensed appendix exists for small models.")
        print("     A 3B model cannot process 6,200 lines of AGENTS.md.")


# ─── RUN ALL ──────────────────────────────────────────────────────────────

def test_toc_discoverability(sections):
    """Verify the TOC actually helps agents find things."""
    print("\n" + "=" * 70)
    print("CROSS-CUTTING: TOC (Table of Contents) Effectiveness")
    print("=" * 70)

    all_text = "\n".join(sections.values())

    has_toc = "Section Index" in all_text
    has_cheatsheet = "Quick-Navigation Cheatsheet" in all_text
    has_anchors = any(f"](#{n.split('.')[0]}" in all_text for n in sections if n[0].isdigit())

    print(f"\n  Section Index (TOC) present: {has_toc}")
    print(f"  Quick-Navigation Cheatsheet present: {has_cheatsheet}")
    print(f"  Anchor links in TOC: {has_anchors}")

    # Count cheatsheet entries
    cheatsheet_lines = all_text.split("Quick-Navigation Cheatsheet")[1].split("---")[0] if has_cheatsheet else ""
    cheatsheet_entries = len(re.findall(r"\| \[(\d+)", cheatsheet_lines))
    print(f"  Cheatsheet entries: {cheatsheet_entries}")

    if has_toc and has_cheatsheet:
        print("\n  ✓ Agents can now navigate non-linearly:")
        print("    1. Scan Section Index to find domain")
        print(f"    2. Or scan {cheatsheet_entries}-entry Quick-Navigation Cheatsheet")
        print("    3. Click anchor link to jump directly to relevant section")


if __name__ == "__main__":
    sections = load_sections()
    section_names = sorted(
        [n for n in sections if n[0].isdigit()],
        key=lambda n: int(n.split(".")[0])
    )
    print(f"AGENTS.md: {len(sections)} sections ({sum(len(t.split(chr(10))) for t in sections.values())} lines)")
    print(f"Numbered sections: {len(section_names)}")

    # Run ORIGINAL scenarios
    test_scenario_1_first_feature(sections)
    test_scenario_2_security_fix(sections)
    test_scenario_3_review_large_pr(sections)
    test_scenario_4_new_project(sections)
    test_scenario_5_flaky_test(sections)
    test_scenario_6_refuse_action(sections)

    # Run NEW stress-test scenarios
    test_scenario_7_simplicity_vs_rigor(sections)
    test_scenario_8_rule_conflict_resolution(sections)
    test_scenario_9_production_incident(sections)
    test_scenario_10_multi_service_system(sections)
    test_scenario_11_legacy_code(sections)
    test_scenario_12_model_capability(sections)

    # Cross-cutting analyses
    test_rule_discoverability(sections)
    test_toc_discoverability(sections)
    test_instruction_depth_overload(sections)
    test_contradiction_risk(sections)
    test_navigational_holes(sections)
    test_verbosity_burden(sections)

    print("\n" + "=" * 70)
    print("COMPLETE — 12 scenarios tested")
    print("=" * 70)
