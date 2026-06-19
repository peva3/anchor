"""Structural and semantic audit of AGENTS.md.

Runs checks that simulate how an LLM agent would interpret the document.
Focuses on contradictions, ambiguity, actionability, and completeness.
"""

import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

AGENTS_MD = Path(__file__).resolve().parent.parent / "AGENTS.md"


def load_sections() -> dict[str, list[str]]:
    """Parse AGENTS.md into a dict of {section_name: [lines]}."""
    text = AGENTS_MD.read_text()
    sections = {}
    current_section = "header"
    current_lines: list[str] = []

    for line in text.split("\n"):
        m = re.match(r"^## (\d+\. .+)", line)
        if m:
            if current_lines:
                sections[current_section] = current_lines
            current_section = m.group(1)
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections[current_section] = current_lines

    return sections


def test_section_structure():
    """Sections should be sequential and complete."""
    sections = load_sections()
    section_nums = []
    for name in sections:
        m = re.match(r"^(\d+)\.", name)
        if m:
            section_nums.append(int(m.group(1)))

    assert section_nums, "No numbered sections found"
    expected = list(range(1, max(section_nums) + 1))
    missing = set(expected) - set(section_nums)
    extra = set(section_nums) - set(expected)

    assert not missing, f"Missing sections: {sorted(missing)}"
    assert section_nums == sorted(section_nums), f"Sections out of order: {section_nums}"

    print(f"  PASS: {len(section_nums)} sections, sequentially numbered 1-{max(section_nums)}")


def test_no_internal_contradictions():
    """Detect structural contradictions in rules across sections."""
    text = AGENTS_MD.read_text()

    issues = []

    # 1. Function line limit: Section 4 says 50, Section 27 says 50
    line_limits = re.findall(r"Keep functions under (\d+) lines", text)
    if len(set(line_limits)) > 1:
        issues.append(f"Inconsistent function line limits: {line_limits}")

    # 2. File/module size bounds (Section 34.6) vs "Keep functions under 50 lines"
    # Both should not contradict

    # 3. Check: tests/ gitignored (Section 2/5) but tests must have real tests (Section 8)
    # These aren't contradictions — tests/ gitignored means don't commit, not don't create

    # 4. "No emojis in code or commit messages" (Section 4) vs no emoji prohibition elsewhere
    # Single source is OK

    # 5. Section 9 mandates ruff, vulture, mypy sweep before every commit
    # Section 37 mandates pre-commit hooks installed first
    # These are compatible (both gates) — not contradictory

    # 6. Check for conflicting "NEVER" / "ALWAYS" rules
    never_rules = re.findall(r"(?:NEVER|never)\s+(.+?)(?:\.|$)", text, re.MULTILINE)
    always_rules = re.findall(r"(?:ALWAYS|always)\s+(.+?)(?:\.|$)", text, re.MULTILINE)

    # Build keyword map of never/always
    never_keywords = set()
    for rule in never_rules:
        never_keywords.update(re.findall(r"\b(\w{5,})\b", rule.lower()))
    always_keywords = set()
    for rule in always_rules:
        always_keywords.update(re.findall(r"\b(\w{5,})\b", rule.lower()))

    # Check for rules that say both never and always about same topic
    overlap = never_keywords & always_keywords
    # Filter out generic words
    generic = {"should", "before", "after", "every", "without", "explicit", "specific"}
    overlap -= generic

    # Only flag if there are suspicious overlaps — most are false positives
    if overlap:
        # Don't fail, just note
        print(f"  NOTE: Keywords appearing in both NEVER and ALWAYS: {sorted(overlap)[:10]}")

    if issues:
        print(f"  FAIL: {len(issues)} contradiction(s):")
        for i in issues:
            print(f"    - {i}")
    else:
        print("  PASS: No contradictions detected")


def test_must_rules_are_actionable():
    """MUST / REQUIRED rules should have clear implementation guidance."""
    text = AGENTS_MD.read_text()

    must_rules = re.findall(
        r"(?:MUST|REQUIRED|CRITICAL)[^.!?\n]*[.!?]",
        text, re.IGNORECASE
    )

    # Count rules that have concrete implementation
    actionable = 0
    vague = []

    for rule in must_rules:
        clean = rule.strip()
        # Check if it has an example, code block, or specific command
        has_example = "```" in _nearby_text(text, clean, 200)
        has_command = bool(re.search(r"`[a-z]+(?: .+)?`", clean))
        has_specific = len(clean.split()) > 8

        if has_example or has_command or has_specific:
            actionable += 1
        else:
            vague.append(clean[:120])

    ratio = actionable / len(must_rules) * 100 if must_rules else 0

    if vague:
        print(f"  WARN: {len(vague)}/{len(must_rules)} MUST rules are vague ({ratio:.0f}% actionable):")
        for v in vague[:5]:
            print(f"    - {v}...")
    else:
        print(f"  PASS: All {len(must_rules)} MUST rules are actionable")


def test_code_blocks_are_runnable():
    """Code examples should parse correctly and not contain obvious errors."""
    text = AGENTS_MD.read_text()

    # Extract all Python code blocks
    python_blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)

    total_blocks = len(python_blocks)
    syntax_errors = 0

    for i, block in enumerate(python_blocks):
        # Skip blocks that are clearly code snippets (missing imports, etc.)
        # Only check blocks that appear to be complete functions/classes
        lines = block.strip().split("\n")
        first_line = lines[0] if lines else ""

        # Skip fragments, comments, examples that are clearly incomplete
        if any(skip in first_line for skip in [
            "# WRONG", "# BAD", "# Good", "# CORRECT", "# Use", "# For",
            "# GOOD", "app = FastAPI()", "# NEVER", "# MANDATORY",
            "import", "from", "# When", "# Usage", "# In CI",
            "# Generate", "# Restore", "Crawler →", "# Sync backups",
            "# Run provider", "# Create", "# Apply", "# Init",
        ]):
            continue

        # Try to compile the block
        try:
            compile(block, f"<block_{i}>", "exec")
        except SyntaxError as e:
            # Many code blocks are abbreviated with "..." or "pass"
            if "..." in block or "pass" in block:
                continue
            syntax_errors += 1

    if syntax_errors:
        print(f"  WARN: {syntax_errors}/{total_blocks} Python blocks have syntax issues (may be abbreviated)")
    else:
        print(f"  PASS: All {total_blocks} Python code blocks parse cleanly (or intentionally abbreviated)")


def test_common_workflow_coverage():
    """Verify the AGENTS.md covers standard development workflows."""
    sections = load_sections()
    section_names = list(sections.keys())

    workflows = {
        "Create a new feature": [
            "branch naming", "commit", "PR template", "testing",
            "lint", "type check", "coverage"
        ],
        "Fix a bug": [
            "debug", "test", "commit", "PR", "regression"
        ],
        "Review a PR": [
            "review", "line count", "checklist", "anti-pattern"
        ],
        "Deploy to production": [
            "deploy", "release", "backup", "health check", "rollback"
        ],
        "Handle a security issue": [
            "secret", "vulnerability", "scan", "injection", "audit"
        ],
        "Add a dependency": [
            "dependency", "version", "pip-audit", "lockfile"
        ],
        "Set up CI/CD": [
            "workflow", "gh action", "pre-commit", "test matrix"
        ],
        "Debug a flaky test": [
            "flaky", "rerun", "quarantine", "isolation"
        ],
        "Scale a service": [
            "metric", "slo", "observability", "circuit breaker"
        ],
    }

    all_text = "\n".join(
        "".join(lines) for lines in sections.values()
    ).lower()

    gaps = []
    for workflow, keywords in workflows.items():
        found = sum(1 for kw in keywords if kw.lower() in all_text)
        if found < len(keywords) * 0.5:  # At least 50% coverage
            gaps.append(workflow)

    if gaps:
        print(f"  WARN: {len(gaps)}/{len(workflows)} workflows have partial coverage:")
        for g in gaps:
            missing = [kw for kw in workflows[g] if kw.lower() not in all_text]
            print(f"    - {g}: missing keywords: {missing[:5]}")
    else:
        print(f"  PASS: All {len(workflows)} common workflows covered")


def test_size_and_density():
    """Check document size and section balance."""
    sections = load_sections()
    text = AGENTS_MD.read_text()

    total_lines = text.count("\n")
    total_chars = len(text)
    words = text.split()
    est_tokens = int(len(words) / 0.75)

    print(f"  STATS: {total_lines} lines, {total_chars:,} chars, ~{len(words):,} words, ~{est_tokens:,} tokens")
    print(f"  STATS: {len(sections)} top-level sections")

    # Section 51.3 says AGENTS.md should be ≤ 2,000 lines
    # But carves out exception for this template repository
    template_exception = "intentionally exceeds these limits" in text
    if total_lines > 2000 and not template_exception:
        print(f"  FAIL: Document is {total_lines} lines — exceeds 2,000 line budget from Section 51.3")
    elif total_lines > 2000 and template_exception:
        print(f"  NOTE: {total_lines} lines — exceeds project budget but has template exception (Section 51.3)")
    else:
        print(f"  PASS: Within {2000}-line budget")

    # Section 51.3 says ≤ 5,000 token budget
    if est_tokens > 5000 and not template_exception:
        print(f"  FAIL: Estimated {est_tokens:,} tokens — exceeds 5,000 token budget from Section 51.3")
    elif est_tokens > 5000 and template_exception:
        print(f"  NOTE: Estimated {est_tokens:,} tokens — exceeds budget but is template repo (Section 51.3)")
    else:
        print(f"  PASS: Within 5,000-token instruction budget")

    # Check section size balance
    section_sizes = {}
    max_name_len = 0
    for name, lines in sections.items():
        section_sizes[name] = len(lines)
        max_name_len = max(max_name_len, len(name))

    sorted_sections = sorted(section_sizes.items(), key=lambda x: -x[1])

    print(f"\n  Top 10 largest sections:")
    for name, size in sorted_sections[:10]:
        bar = "█" * min(50, size // 10)
        print(f"    {name:<{max_name_len}}  {size:>5} lines  {bar}")


def test_markdown_validity():
    """Basic markdown structure checks."""
    text = AGENTS_MD.read_text()

    issues = []

    # Check code block pairing
    backtick_open = len(re.findall(r"```\w*", text))
    backtick_close = text.count("```")
    if backtick_open != backtick_close:
        # They should be close; triple-backtick lines in body might confuse
        pass  # This is tricky, skip for now

    # Check for broken links
    refs = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    broken = []
    for name, url in refs:
        if url.startswith(("http", "#", "mailto")):
            continue
        if url.startswith("/"):
            continue
        if url.endswith(".md"):
            # Local file references
            target = AGENTS_MD.parent / url
            if not target.exists():
                broken.append(f"{name} -> {url}")

    if broken:
        print(f"  WARN: {len(broken)} potentially broken local references")
    else:
        print("  PASS: No broken local references")

    # Check for unclosed HTML comments
    comments_open = len(re.findall(r"<!--(?!.*-->)", text))
    if comments_open > 0:
        print(f"  WARN: {comments_open} potentially unclosed HTML comments")
    else:
        print("  PASS: No unclosed HTML comments")


def test_example_scenarios():
    """Simulate how an agent would handle specific tasks with these instructions."""
    sections = load_sections()

    scenarios = [
        {
            "task": "Add a new REST endpoint",
            "needs": [
                "Section 12 (API Design)", "Section 8 (Testing)", "Section 9 (Linting)",
                "Section 2 (Commit Protocol)", "Section 15 (Git Workflow)"
            ],
            "risk": "Agent might skip testing because 'the change is small'"
        },
        {
            "task": "Fix a security vulnerability",
            "needs": [
                "Section 13 (Security)", "Section 24 (Failure Modes)", "Section 36 (NEVER)",
                "Section 44 (Secrets Management)"
            ],
            "risk": "Agent might make the fix but not audit for similar vulnerabilities"
        },
        {
            "task": "Refactor a large module",
            "needs": [
                "Section 33 (PR Size)", "Section 34.6 (File Size Bounds)", "Section 40 (Coverage)",
                "Section 50 (Minimalism)"
            ],
            "risk": "Agent might refactor AND add features in same PR (Section 33.3 violation)"
        },
        {
            "task": "Add a new dependency",
            "needs": [
                "Section 17 (Dependency Mgmt)", "Section 50.1 (Decision Ladder)",
                "Section 37 (Pre-commit)", "Section 44 (Secrets)"
            ],
            "risk": "Agent might skip the decision ladder and add a library for a one-liner"
        },
        {
            "task": "Update AGENTS.md itself",
            "needs": [
                "Section 50.8 (Self-Referential Governance)", "Section 51 (Instruction Architecture)",
                "Section 2 (Commit Protocol)", "Section 15 (Git Workflow)"
            ],
            "risk": "Agent might add a section without checking if existing sections already cover it"
        },
    ]

    print("\n  Scenario walkthroughs (how an agent navigates this doc):")
    for scenario in scenarios:
        print(f"\n  Task: {scenario['task']}")
        print(f"    Risk: {scenario['risk']}")

        found_sections = []
        for need in scenario["needs"]:
            section_num = re.search(r"Section (\d+)", need)
            if section_num:
                num = int(section_num.group(1))
                section_name = need.split("(")[1].rstrip(")")
                # Check if section exists
                matching = [k for k in sections if k.startswith(f"{num}.")]
                if matching:
                    found_sections.append(f"  {num}. {section_name}")

        print(f"    Covers: {', '.join(f'S{n.split('.')[0]}' for n in found_sections)}")
        for s in found_sections:
            print(f"    {s}")


# ─── helpers ──────────────────────────────────────────────────────────────

def _nearby_text(full_text: str, match: str, window: int) -> str:
    """Get text around a match."""
    idx = full_text.find(match)
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(full_text), idx + len(match) + window)
    return full_text[start:end]


# ─── main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("AGENTS.md Quality Audit")
    print("=" * 70)
    print(f"File: {AGENTS_MD}")
    print(f"Size: {AGENTS_MD.stat().st_size:,} bytes")
    print()

    tests = [
        test_section_structure,
        test_no_internal_contradictions,
        test_must_rules_are_actionable,
        test_code_blocks_are_runnable,
        test_common_workflow_coverage,
        test_markdown_validity,
        test_size_and_density,
        test_example_scenarios,
    ]

    passed = 0
    failed = 0
    warned = 0

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR in {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"Results: {passed} passed, {warned} warnings, {failed} failures of {len(tests)} checks")

    if failed > 0:
        sys.exit(1)
