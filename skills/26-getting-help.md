# Skill 26: Getting Help

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 26. Getting Help

When stuck on a problem.

### 26.1 Self-Service First

1. Check project documentation in `/docs/`
2. Search `/research/` for similar patterns or whitepapers
3. Review past commits for similar fixes: `git log --grep="keyword"`
4. Run linting/smoke tests — actual errors often reveal the issue
5. Search codebase with `grep -r "pattern" .` for similar implementations

### 26.2 Framework-Specific Resources

```
LangChain:    https://docs.langchain.com/
AutoGPT:      https://docs.agpt.co/
CAMEL:        https://docs.camel-ai.org/
MetaGPT:      https://deepwisdom.com/
Anthropic:   https://docs.anthropic.com/
OpenAI:      https://platform.openai.com/docs/
```

### 26.3 When to Escalate

Ask the user when:
- Problem requires making decisions with trade-offs (not clear cut)
- Fix requires changing architecture rather than code
- Issue is not in code but in requirements/expectations
- You've been stuck for more than 15 minutes with no progress

### 26.4 How to Ask for Help

When escalating, provide:
- What you were trying to do
- What you tried
- What happened vs what expected
- Relevant error messages or logs

---

