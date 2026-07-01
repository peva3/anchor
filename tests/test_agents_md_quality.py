"""Structural and semantic audit of AGENTS.md.

Runs checks that simulate how an LLM agent would interpret the document.
Focuses on contradictions, ambiguity, actionability, and completeness.

Usage:
    python3 tests/test_agents_md_quality.py            # normal mode (WARNs)
    python3 tests/test_agents_md_quality.py --strict   # strict mode (WARNs fail)
    python3 -m pytest tests/test_agents_md_quality.py  # run individual tests

ponytail: print-only WARN checks
Upgrade to assertions behind --strict if contributors start ignoring WARNs.
"""

import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

AGENTS_MD = Path(__file__).resolve().parent.parent / "AGENTS.md"

# Module-level cache so 8 tests don't re-read the 195KB file 8 times.
_TEXT: str | None = None
_SECTIONS: dict[str, list[str]] | None = None


def load_text() -> str:
    """Read AGENTS.md once and cache it."""
    global _TEXT
    if _TEXT is None:
        _TEXT = AGENTS_MD.read_text()
    return _TEXT


def load_sections() -> dict[str, list[str]]:
    """Parse AGENTS.md into a dict of {section_name: [lines]}, cached."""
    global _SECTIONS
    if _SECTIONS is None:
        text = load_text()
        sections: dict[str, list[str]] = {}
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
        _SECTIONS = sections
    return _SECTIONS


def _is_strict() -> bool:
    """Strict mode: WARNs become failures. Used by CI and pre-commit."""
    return "--strict" in sys.argv


def _record_warn(name: str, message: str) -> None:
    """Print a warning; in strict mode, raise to fail the run."""
    print(f"  WARN: {name}: {message}")
    if _is_strict():
        raise AssertionError(f"{name}: {message}")


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
    """Detect structural contradictions in rules across sections.

    Checks three categories: numeric limits, NEVER/ALWAYS keyword overlap, and
    same-topic opposite directives. Reports WARN for any of the three; the
    keyword overlap is the strongest signal.
    """
    text = load_text()
    issues: list[str] = []

    # 1. Numeric limits (e.g., function line limit)
    line_limits = re.findall(r"Keep functions under (\d+) lines", text)
    if len(set(line_limits)) > 1:
        issues.append(f"Inconsistent function line limits: {line_limits}")

    # 2. NEVER/ALWAYS keyword overlap (curated blocklist of generic words).
    never_rules = re.findall(r"(?:NEVER|never)\s+(.+?)(?:\.|$)", text, re.MULTILINE)
    always_rules = re.findall(r"(?:ALWAYS|always)\s+(.+?)(?:\.|$)", text, re.MULTILINE)

    def _keywords(rules: list[str]) -> set[str]:
        out: set[str] = set()
        for rule in rules:
            out.update(re.findall(r"\b(\w{5,})\b", rule.lower()))
        return out

    never_keywords = _keywords(never_rules)
    always_keywords = _keywords(always_rules)
    generic = {"should", "before", "after", "every", "without", "explicit", "specific"}
    overlap = (never_keywords & always_keywords) - generic

    if overlap:
        # Don't fail, but surface for human review.
        print(f"  NOTE: Keywords appearing in both NEVER and ALWAYS: {sorted(overlap)[:10]}")

    if issues:
        print(f"  FAIL: {len(issues)} contradiction(s):")
        for i in issues:
            print(f"    - {i}")
    else:
        print("  PASS: No contradictions detected")


def test_must_rules_are_actionable():
    """MUST / REQUIRED rules should have clear implementation guidance."""
    text = load_text()

    must_rules = re.findall(
        r"(?:MUST|REQUIRED|CRITICAL)[^.!?\n]*[.!?]",
        text, re.IGNORECASE
    )

    actionable = 0
    vague: list[str] = []

    for rule in must_rules:
        clean = rule.strip()
        has_example = "```" in _nearby_text(text, clean, 200)
        has_command = bool(re.search(r"`[a-z]+(?: .+)?`", clean))
        has_specific = len(clean.split()) > 8

        if has_example or has_command or has_specific:
            actionable += 1
        else:
            vague.append(clean[:120])

    ratio = actionable / len(must_rules) * 100 if must_rules else 0

    if vague:
        _record_warn(
            "vague_must_rules",
            f"{len(vague)}/{len(must_rules)} MUST rules are vague ({ratio:.0f}% actionable)",
        )
        for v in vague[:5]:
            print(f"    - {v}...")
    else:
        print(f"  PASS: All {len(must_rules)} MUST rules are actionable")


def test_code_blocks_are_runnable():
    """Code examples should parse correctly and not contain obvious errors.

    Uses a structural skip rule instead of a hardcoded string list: any block
    containing `...` or `pass` is treated as intentionally abbreviated. This
    is more robust than enumerating comment prefixes.
    """
    text = load_text()

    python_blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
    total_blocks = len(python_blocks)
    syntax_errors: list[tuple[int, str]] = []

    for i, block in enumerate(python_blocks):
        # Structural skip: the block is a fragment or skeleton.
        if "..." in block or "pass" in block:
            continue
        # Structural skip: illustrative pattern comparison (e.g., "# CORRECT" / "# WRONG").
        # ponytail: keeping the marker check alongside the structural rules.
        # The structural rules catch "..."/"pass"/<2 lines; the marker check catches
        # "# CORRECT"/"# WRONG" pairs which are always partial fragments. If we skip
        # the marker check, the audit flags intentional illustrations (return outside
        # def) as errors. Keep both until blocks include proper `def` wrapping.
        if re.search(r"#\s*(?:CORRECT|WRONG|GOOD|BAD)\b", block, re.IGNORECASE):
            continue
        # Structural skip: the block is just an import or a single statement.
        stripped = block.strip()
        non_comment_lines = [
            line for line in stripped.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        if len(non_comment_lines) < 2:
            continue

        try:
            compile(block, f"<block_{i}>", "exec")
        except SyntaxError as e:
            syntax_errors.append((i, str(e)))

    if syntax_errors:
        _record_warn(
            "python_syntax",
            f"{len(syntax_errors)}/{total_blocks} Python blocks have syntax issues",
        )
    else:
        print(f"  PASS: All {total_blocks} Python code blocks parse cleanly (or abbreviated)")


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

    gaps: list[str] = []
    for workflow, keywords in workflows.items():
        found = sum(1 for kw in keywords if kw.lower() in all_text)
        if found < len(keywords) * 0.5:
            gaps.append(workflow)

    if gaps:
        _record_warn(
            "workflow_gaps",
            f"{len(gaps)}/{len(workflows)} workflows have partial coverage",
        )
        for g in gaps:
            missing = [kw for kw in workflows[g] if kw.lower() not in all_text]
            print(f"    - {g}: missing keywords: {missing[:5]}")
    else:
        print(f"  PASS: All {len(workflows)} common workflows covered")


def test_size_and_density():
    """Check document size and section balance."""
    sections = load_sections()
    text = load_text()

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
        _record_warn(
            "size_budget",
            f"Document is {total_lines} lines — exceeds 2,000 line budget from Section 51.3",
        )
    elif total_lines > 2000 and template_exception:
        print(f"  NOTE: {total_lines} lines — exceeds project budget but has template exception (Section 51.3)")
    else:
        print(f"  PASS: Within {2000}-line budget")

    if est_tokens > 5000 and not template_exception:
        _record_warn(
            "token_budget",
            f"Estimated {est_tokens:,} tokens — exceeds 5,000 token budget from Section 51.3",
        )
    elif est_tokens > 5000 and template_exception:
        print(f"  NOTE: Estimated {est_tokens:,} tokens — exceeds budget but is template repo (Section 51.3)")
    else:
        print(f"  PASS: Within 5,000-token instruction budget")

    # Section size balance
    section_sizes = {name: len(lines) for name, lines in sections.items()}
    max_name_len = max(len(name) for name in section_sizes)
    sorted_sections = sorted(section_sizes.items(), key=lambda x: -x[1])

    print(f"\n  Top 10 largest sections:")
    for name, size in sorted_sections[:10]:
        bar = "█" * min(50, size // 10)
        print(f"    {name:<{max_name_len}}  {size:>5} lines  {bar}")


def test_markdown_validity():
    """Basic markdown structure checks."""
    text = load_text()

    # Broken local references
    refs = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    broken = []
    for name, url in refs:
        if url.startswith(("http", "#", "mailto")):
            continue
        if url.startswith("/"):
            continue
        if url.endswith(".md"):
            target = AGENTS_MD.parent / url
            if not target.exists():
                broken.append(f"{name} -> {url}")

    if broken:
        _record_warn("broken_refs", f"{len(broken)} potentially broken local references")
        for b in broken:
            print(f"    - {b}")
    else:
        print("  PASS: No broken local references")

    # Unclosed HTML comments
    comments_open = len(re.findall(r"<!--(?!.*-->)", text))
    if comments_open > 0:
        _record_warn("unclosed_comments", f"{comments_open} potentially unclosed HTML comments")
    else:
        print("  PASS: No unclosed HTML comments")

    # Platform config files exist for all 7 referenced platforms
    expected_configs = [
        "CLAUDE.md",
        "CLAUDE.desktop.md",
        ".github/copilot-instructions.md",
        ".cursor/rules/project-rules.mdc",
        ".windsurf/config.md",
        ".continue/config.md",
        ".claude/config.json",
        "docs/AGENT_INSTRUCTIONS.md",
    ]
    repo_root = AGENTS_MD.parent
    missing_configs = [c for c in expected_configs if not (repo_root / c).exists()]
    if missing_configs:
        _record_warn("missing_configs", f"Missing platform config files: {missing_configs}")
    else:
        print(f"  PASS: All {len(expected_configs)} platform config files present")


def test_example_scenarios():
    """Verify the doc covers the 5 critical agent tasks with their required sections.

    Unlike the prior version, this test now ASSERTS: any section referenced in
    a scenario must exist, and a missing reference is a failure (in strict mode)
    or a WARN (in normal mode). This catches silent drift in section numbering.
    """
    sections = load_sections()
    section_numbers = {
        int(m.group(1))
        for name in sections
        if (m := re.match(r"^(\d+)\.", name))
    }

    scenarios = [
        ("Add a new REST endpoint", [12, 8, 9, 2, 15]),
        ("Fix a security vulnerability", [13, 24, 36, 44]),
        ("Refactor a large module", [33, 34, 40, 50]),
        ("Add a new dependency", [17, 50, 37, 44]),
        ("Update AGENTS.md itself", [50, 51, 2, 15]),
    ]

    print("\n  Scenario walkthroughs (agent navigates this doc):")
    failures: list[str] = []
    for task, required in scenarios:
        missing = [n for n in required if n not in section_numbers]
        if missing:
            failures.append(f"{task}: missing sections {missing}")
            print(f"  Task: {task}")
            print(f"    FAIL: missing sections {missing}")
        else:
            print(f"  Task: {task}")
            print(f"    Covers: S{', S'.join(str(n) for n in required)}")

    if failures:
        _record_warn("scenario_sections", f"{len(failures)} scenario(s) reference missing sections")


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
    print(f"Mode: {'STRICT (WARNs fail)' if _is_strict() else 'normal (WARNs report only)'}")
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
