---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- skill-07's description is named as the biggest always-paid cost (or ranked first)
- skill-03's large inline code block is flagged as something to move out or script
- skill-11's reference file is flagged as unlinked (never loaded)
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: skill-07 has a description of several hundred words, paid every session; skill-03 carries a 120-line code block in SKILL.md; skill-11/reference.md is not linked from its SKILL.md. The other nine skills are small and clean.
