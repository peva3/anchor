"""LLM behavioral simulation tests for AGENTS.md.

Simulates how differently-configured LLMs would interpret and apply
the rules in AGENTS.md. Tests for: ambiguity, over-enforcement,
under-enforcement, context confusion, scope errors, and chaining.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

AGENTS_MD = Path(__file__).resolve().parent.parent / "AGENTS.md"


class SimulatedAgent:
    """Simulates an LLM agent with a specific reading strategy."""

    def __init__(self, name: str, strategy: str, context_window: int = 8000):
        self.name = name
        self.strategy = strategy
        self.context_window = context_window
        self.text = AGENTS_MD.read_text()
        self.sections = self._parse_sections()
        self.all_text_lower = self.text.lower()

    def _parse_sections(self) -> dict[str, str]:
        sections = {}
        current_section = "header"
        current_text: list[str] = []
        for line in self.text.split("\n"):
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

    def read_header_only(self) -> str:
        """Scan-only agent: reads just the header area."""
        return self.sections.get("header", "")

    def read_first_sections(self, n: int = 10) -> str:
        """Skims-first agent: reads first N sections then stops."""
        names = sorted(
            [k for k in self.sections if k[0].isdigit()],
            key=lambda x: int(x.split(".")[0])
        )
        text = self.sections.get("header", "")
        for name in names[:n]:
            text += "\n" + self.sections.get(name, "")
        return text

    def search_keyword(self, keyword: str) -> list[str]:
        """Search agent: searches for keyword, reads matching sections."""
        return [
            name for name, text in self.sections.items()
            if re.search(keyword, text, re.IGNORECASE)
        ]

    def read_range(self, start: int, end: int) -> str:
        """Sequential reader: reads sections start through end."""
        names = sorted(
            [k for k in self.sections if k[0].isdigit()],
            key=lambda x: int(x.split(".")[0])
        )
        text = ""
        for name in names:
            num = int(name.split(".")[0])
            if start <= num <= end:
                text += "\n" + self.sections.get(name, "")
        return text


# ─── AGENT TYPES ──────────────────────────────────────────────────────────

def create_agents():
    """Create simulated agents with different reading strategies."""
    return {
        "Scanner": SimulatedAgent(
            "Scanner",
            "Reads header/TOC only, then keyword-searches",
            context_window=8000
        ),
        "Skimmer": SimulatedAgent(
            "Skimmer",
            "Reads first 10 sections, assumes rest is detail",
            context_window=8000
        ),
        "DeepReader": SimulatedAgent(
            "DeepReader",
            "Reads linearly from section 1 onward, limited by window",
            context_window=12000
        ),
        "KeywordJumper": SimulatedAgent(
            "KeywordJumper",
            "Picks keywords from task, jumps to matching sections",
            context_window=4000
        ),
        "SmallModel": SimulatedAgent(
            "SmallModel",
            "Can only read first 20 sections due to context budget",
            context_window=4000
        ),
    }


# ─── TEST 1: Does the cheatsheet/TOC prevent over-enforcement? ────────────

def test_toc_prevents_scope_confusion():
    """If an agent reads the header+TOC, does it realize this is a TEMPLATE
    (not rules it must enforce on itself right now)?"""
    print("=" * 70)
    print("TEST 1: TOC prevents scope confusion")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)
    header = agent.read_header_only()

    issues = []

    # Check: does the header clearly state "adapt to YOUR project"?
    has_adapt = "adapt" in header.lower() and "project" in header.lower()
    print(f"\n  Header says 'adapt to project': {has_adapt}")
    if not has_adapt:
        issues.append("Header doesn't clearly say to adapt to project scope")

    # Check: does the TOC make it clear sections are OPTIONAL to keep?
    toc_area = header.lower()
    has_trim = "trim" in toc_area or "keep only" in toc_area or "delete" in toc_area
    print(f"  TOC mentions trimming/deleting sections: {has_trim}")

    # Check: Section 51.3 template exception
    section_51 = agent.sections.get(
        "51. Instruction Architecture — Context Economy & Self-Improvement", ""
    )
    has_exception = "template library" in section_51.lower() or "intentionally exceeds" in section_51.lower()
    print(f"  Section 51.3 has template exception: {has_exception}")

    # KEY CHECK: If agent reads only header+TOC, does it know not to apply
    # ALL 52 sections to every project?
    if has_adapt and has_trim:
        print("\n  ✓ Agent reading header+TOC would know to trim sections")
    else:
        print(f"\n  ❌ Agent might apply 52 sections to a 3-file project")


# ─── TEST 2: Word boundary disambiguation ─────────────────────────────────

def test_word_boundary_disambiguation():
    """Does the agent confuse similarly-named concepts?"""
    print("\n" + "=" * 70)
    print("TEST 2: Word boundary disambiguation")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)

    # These search queries could return wrong sections
    ambiguous = [
        # query -> correct section, wrong-section-it-might-hit
        ("contract test", "48. Contract Testing", "eventual consistency, transaction boundaries"),
        ("flaky test", "45. Flaky Test Management", "end-to-end testing, race conditions"),
        ("PR size", "33. PR & Change Size Standards", "docker image size, binary size"),
        ("dead code", "9. Linting & Type Checking", "dead letter queue, circuit breaker dead"),
        ("rule enforcement", "52. Rule Enforcement Architecture", "pre-commit hooks rule enforcement"),
    ]

    print()
    issues = []
    for query, correct, wrong_guess in ambiguous:
        results = agent.search_keyword(query)
        correct_found = any(correct in r for r in results)
        # Check if the agent would land on the RIGHT first match
        if results:
            top_hit = results[0]
            correct_first = correct in top_hit
            if not correct_first:
                issues.append(f"'{query}' → first hit is '{top_hit}', should be '{correct}'")

    if issues:
        for i in issues:
            print(f"  ⚠️  {i}")
    else:
        print("  ✓ All keyword searches land on correct sections")


# ─── TEST 3: Chaining — does agent follow cross-references? ──────────────

def test_cross_reference_chaining():
    """When an agent reads Section 1 which says 'see Section 9 for HOW',
    does it actually jump to Section 9? And does Section 9 have what it needs?"""
    print("\n" + "=" * 70)
    print("TEST 3: Cross-reference chain integrity")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)

    # Test the chain: Section 1 says "Section 9 — vulture sweep"
    # → Agent jumps to Section 9
    # → Section 9 should have concrete, runnable commands
    section_9 = agent.sections.get("9. Linting & Type Checking", "")

    has_runnable = "ruff check" in section_9 and "vulture" in section_9
    print(f"\n  Section 9 has runnable commands: {has_runnable}")

    # Cross-ref: Section 1 says "How: Section 8" for test validation
    section_8 = agent.sections.get("8. Testing Requirements", "")
    has_test_command = "pytest" in section_8
    print(f"  Section 8 has test commands: {has_test_command}")

    # Cross-ref: Section 50.3 says "security" is exempt
    # → Agent should check Section 13 for what security means
    section_50 = agent.sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    section_13 = agent.sections.get("13. Security Best Practices", "")
    section_50_mentions_security = "security" in section_50.lower() and "exempt" in section_50.lower()
    section_13_has_detail = "input validation" in section_13.lower() and "parameterized" in section_13.lower()
    print(f"  Chain: S50→S13 exists: {section_50_mentions_security}")
    print(f"  Chain: S13 has detail agent needs: {section_13_has_detail}")

    if has_runnable and has_test_command and section_50_mentions_security and section_13_has_detail:
        print("\n  ✓ All cross-reference chains are complete")
    else:
        print("\n  ❌ Broken cross-reference chain detected")


# ─── TEST 4: Boundary case — when rules are too strict ────────────────────

def test_rules_too_strict_boundary():
    """Does the agent refuse reasonable requests because of overly strict interpretation?"""
    print("\n" + "=" * 70)
    print("TEST 4: Over-enforcement boundary check")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)

    scenarios = [
        {
            "user_says": "Push this one-line typo fix to main, it's urgent",
            "rule": "Section 33 says max 800 lines AND single feature per PR",
            "correct_behavior": "Apply the rule literally — 1 line is under 800, push it",
            "risk": "Agent might refuse because 1 line doesn't have tests (Section 50.7 exempts trivial one-liners)"
        },
        {
            "user_says": "Just add a print statement for debugging",
            "rule": "Section 4 says no print statements, use logging",
            "correct_behavior": "Add the print — EXPLICIT user request takes priority over style rules (Section 50.3)",
            "risk": "Agent might refuse the user's explicit request and lecture about logging"
        },
        {
            "user_says": "Skip tests for this prototype, I'll add them later",
            "rule": "Section 1 says test-first, Section 8 says tests required",
            "correct_behavior": "Accept user's explicit instruction. Add a tradeoff comment (Section 50.2) naming what's missing",
            "risk": "Agent might refuse to proceed without tests, blocking the user"
        },
        {
            "user_says": "Close this issue, the bug is invalid",
            "rule": "Section 2 / 36.3 says never close issues without approval",
            "correct_behavior": "The user just gave approval — close it. The rule says 'without approval', not 'never ever'",
            "risk": "Agent might refuse to close the issue even though user explicitly asked"
        },
    ]

    section_50 = agent.sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    section_2 = agent.sections.get("2. Commit Protocol", "")

    print()
    for sc in scenarios:
        print(f"  User: '{sc['user_says']}'")
        print(f"  Rule: {sc['rule']}")
        print(f"  Correct: {sc['correct_behavior']}")
        print(f"  Risk: {sc['risk']}")

        # Check: does the safety carve-out cover this?
        has_explicit_request_carve = "explicitly requested" in section_50.lower()
        print(f"  Safety carve-out for explicit requests exists: {has_explicit_request_carve}")
        print()


# ─── TEST 5: Section 50 vs Section 15 resolution ─────────────────────────

def test_commit_rule_priority():
    """Does Section 50.4 (≤3 lines) ever override Section 15 (detailed WHY)? """
    print("=" * 70)
    print("TEST 5: Commit message rule priority")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)
    section_50 = agent.sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    section_15 = agent.sections.get("15. Git Workflow", "")

    # Section 50.4 says: "three short lines: what was skipped, when to add it"
    # Section 15 says: "problem → solution → context"
    # Which applies when?

    # Check: does Section 50.4 explicitly scope itself to non-commit output?
    has_output_scope = "presenting completed work" in section_50.lower()
    has_commit_exception = "commit" in section_50.lower() and "exception" in section_50.lower()

    print(f"\n  Section 50.4 scopes to 'completed work' output: {has_output_scope}")
    print(f"  Section 50.4 explicitly excludes commits: {has_commit_exception}")

    if not has_commit_exception:
        print("\n  ⚠️  RISK: Section 50.4 says 'at most three short lines' for output.")
        print("     Without explicit commit exclusion, agent might apply this to commits.")
        print("     Add: 'This does NOT apply to commit messages — see Section 15.'")

    # Check: does Section 15 know about Section 50.4?
    mentions_50 = "section 50" in section_15.lower() or "50.4" in section_15.lower()
    print(f"  Section 15 references Section 50: {mentions_50}")

    # Check: cheatsheet — what does it tell agent about commit messages?
    header = agent.read_header_only()
    cheatsheet_says = "Committ code" if "Commit code" in header else "not in cheatsheet"
    print(f"  Cheatsheet entry for commits: {cheatsheet_says}")


# ─── TEST 6: Sequential-section agent misses late rules ───────────────────

def test_sequential_reader_misses_late_rules():
    """If an agent reads sections 1-10 and stops (common LLM behavior),
    what critical rules does it MISS?"""
    print("\n" + "=" * 70)
    print("TEST 6: Sequential reader gap analysis (reads 1-10, stops)")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)
    early_text = agent.read_first_sections(10)
    full_text = agent.text

    # Rules that ONLY appear in sections > 10
    late_only_rules = []

    # What does the agent miss?
    checks = [
        ("PR size limit (800 lines)", "800.line|800 lines", 33),
        ("NEVER list", "explicit.prohibition", 36),
        ("Decision ladder", "yagni.*stdlib", 50),
        ("Flaky test quarantine", "quarantine|rerunfailures", 45),
        ("Contract testing", "pact.*contract", 48),
        ("Secret rotation", "rotate.*secret", 44),
        ("Database backup strategy", "backup.*retention|grandfather", 43),
        ("Enforcement architecture", "two.layer.*enforcement", 52),
        ("Evidence-first methodology", "file:line.*citation", 52),
        ("CI/CD workflows", "ci\\.yml|workflow", 38),
    ]

    print()
    missing = []
    for rule_name, keyword, min_section in checks:
        in_early = bool(re.search(keyword, early_text, re.IGNORECASE))
        if not in_early:
            missing.append(rule_name)
            print(f"  ❌ MISSED: {rule_name} (first appears in Section {min_section})")
        else:
            print(f"  ✓ FOUND: {rule_name}")

    # KEY FINDING: does the TOC fix this?
    if missing:
        print(f"\n  ⚠️  Agent reading only Sections 1-10 misses {len(missing)}/{len(checks)} critical rules.")
        print("     THE FIX: TOC + cheatsheet in header. Agent scanning header sees domain map.")
        header = agent.read_header_only()
        has_toc = "Section Index" in header
        has_cheatsheet = "Quick-Navigation Cheatsheet" in header
        print(f"     TOC in header: {has_toc}")
        print(f"     Cheatsheet in header: {has_cheatsheet}")
        if has_toc and has_cheatsheet:
            print("     ✓ Even sequential reader sees TOC in header and can jump.")


# ─── TEST 7: Negative space — what common tasks have NO guidance ──────────

def test_negative_space_analysis():
    """What would an agent search for and find NOTHING?"""
    print("\n" + "=" * 70)
    print("TEST 7: Negative space — common queries with zero results")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)

    queries = [
        ("How do I set up database migrations?", "alembic.*migration|flyway|migrate.*database.*new"),
        ("How do I version an API?", "api.*version|versioning.*api|/v1/|/v2/"),
        ("How do I set up monitoring dashboards?", "grafana|dashboard|monitoring.*dashboard"),
        ("How do I do code generation?", "code.*generat|protobuf|openapi.*generat"),
        ("How do I handle user authentication?", "authentication|auth.*flow|oauth.*flow|login.*flow"),
        ("How do I handle rate limiting?", "rate.*limit.*details|throttle.*specific"),
        ("How do I set up logging levels?", "log.*level.*config|logging.*config.*example"),
        ("How do I handle file uploads?", "file.*upload|multipart|upload.*size.*limit"),
        ("How do I do dependency injection?", "dependency.*injection|DI.*container|inject.*depend"),
        ("How do I configure CORS?", "cors|cross.origin|cross-origin"),
    ]

    print()
    missing = []
    for query, keyword in queries:
        results = agent.search_keyword(keyword)
        if not results:
            missing.append(query)
            print(f"  ❌ NO RESULTS: {query}")
        else:
            print(f"  ✓ {query} → {results[0]}")

    if missing:
        print(f"\n  ⚠️  {len(missing)}/{len(queries)} common queries have NO guidance in AGENTS.md")
        print("     These may be intentionally out of scope (project-specific) or missing gaps.")
    else:
        print(f"\n  ✓ All {len(queries)} queries find relevant sections")


# ─── TEST 8: LLM literal interpretation traps ─────────────────────────────

def test_literal_interpretation_traps():
    """LLMs take instructions literally. Are there ambiguous phrases
    that would cause an LLM to do exactly the wrong thing?"""
    print("\n" + "=" * 70)
    print("TEST 8: Literal interpretation traps")
    print("=" * 70)

    agent = SimulatedAgent("test", "", 8000)

    traps = [
        (
            "Section 50.1 Rung 5: 'One line. Do not write a function.'",
            "LLM might inline EVERYTHING, even complex expressions that are unreadable",
            r"one.line.*do.not.*write|one line.*self-documenting"
        ),
        (
            "Section 2: 'automatically commit and push the changes'",
            "LLM might auto-commit halfway through a feature, breaking atomicity",
            r"automatically.*commit.*push"
        ),
        (
            "Section 50.4: 'If explanation longer than code, delete the explanation'",
            "LLM might delete a critical security explanation because the code is shorter",
            r"delete the explanation"
        ),
        (
            "Section 52.5: 'Every assertion must cite file:line'",
            "LLM might refuse to make ANY assertion without finding the exact line first",
            r"every.*claim.*must.*cite.*file"
        ),
    ]

    print()
    for phrase, risk, keyword in traps:
        results = agent.search_keyword(keyword)
        found = len(results) > 0
        print(f"  Phrase: '{phrase[:60]}...'")
        print(f"  Risk: {risk}")
        print(f"  Found in sections: {', '.join(results[:2])}")
        print()

    # Check: are there counter-balancing safeguards?
    section_50 = agent.sections.get("50. Intentional Minimalism — The Simplicity-First Architecture", "")
    safeguards = [
        "when should NOT" in section_50.lower(),
        "exception" in section_50.lower(),
        "explicitly requested" in section_50.lower(),
    ]
    print(f"  Safeguards against literal over-application: {sum(safeguards)}/3 present")
    if sum(safeguards) < 3:
        print(f"  ⚠️  Missing counter-balancing language in Section 50")


# ─── RUN ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("AGENTS.md LLM Behavioral Simulation")
    print(f"File: {AGENTS_MD}")
    print(f"Size: {AGENTS_MD.stat().st_size:,} bytes\n")
    print("Simulating 4 agent types with different reading strategies:\n")
    print("  Scanner — reads TOC only, keyword-searches for tasks")
    print("  Skimmer — reads sections 1-10, assumes rest is detail")
    print("  DeepReader — reads linearly, limited by context window")
    print("  KeywordJumper — keyword-driven, small context budget")
    print("  SmallModel — 4K context, can only read sections 1-20\n")

    test_toc_prevents_scope_confusion()
    test_word_boundary_disambiguation()
    test_cross_reference_chaining()
    test_rules_too_strict_boundary()
    test_commit_rule_priority()
    test_sequential_reader_misses_late_rules()
    test_negative_space_analysis()
    test_literal_interpretation_traps()

    print("\n" + "=" * 70)
    print("COMPLETE — 8 behavioral simulations done")
    print("=" * 70)
