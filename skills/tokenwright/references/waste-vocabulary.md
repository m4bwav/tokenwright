# Waste vocabulary

Lean manufacturing names seven kinds of waste. Each has a token form. Ideas paraphrased from Ohno, *Toyota Production System* (1988), Womack and Jones, *Lean Thinking*, and Goldratt, *The Goal*; notes and chapter citations live in the book-learnings notes, not here.

| Waste | Token form | tw.py kind | Fix family |
|---|---|---|---|
| Transport | Data moved into context and barely used: whole files for three lines, raw logs, full JSON | `whole-read`, `shell-cat`, `big-output` | 1 Don't load |
| Motion | Reading the same thing twice; a duplicate search | `repeat read`, `re-read after own edit` | 1 Don't reload |
| Defects | A failed call sent again unchanged | `retry` | Stop at the first error and diagnose |
| Overproduction | Output nobody reads: recaps, dumps in replies, a report when one line was wanted | (reply length; not scored yet) | Output side |
| Inventory | Loaded but never used: skill descriptions, MCP schemas, files read "just in case" | `tw.py skill` | 1 and skill review |
| Waiting | Serial turns that could have been one batched turn; polling loops | (not scored yet) | 2 Shortcut |
| Overprocessing | Work past what the answer needs: re-verifying settled facts, gold-plating | (not scored) | 2 Shortcut |

Overproduction is the worst, because it hides the others: a long dump makes the next turn's real need hard to see.

## Rules borrowed from the books

- **Find the bottleneck first** (Goldratt's five focusing steps): measure, fix the largest sink, make the rest serve that fix, make it structural, measure again. A saving away from the bottleneck changes little.
- **Pull, not push**: load what the next step asks for (outline, then section), not what might be useful.
- **Stop the line** (jidoka): at the first error, stop and read it. Never resend.
- **Standard work where the work happens**: write the script from the commands that actually worked, not from a plan.
- **Value stream**: sort each step into adds value, needed for now, removable now. Cut the third group first.
- **Capacity = work + waste**: report waste as a share of what was spent.
