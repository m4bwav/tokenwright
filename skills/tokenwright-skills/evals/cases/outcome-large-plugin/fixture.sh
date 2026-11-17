#!/usr/bin/env bash
# Generate a 12-skill plugin with three planted costs (see graders/judge.md).
set -e
B=evals/fixtures/big-plugin
mkdir -p $B
printf '{"name":"big-plugin","version":"1.0.0","skills":"./skills"}\n' > $B/plugin.json
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do
  d=$B/skills/skill-$i; mkdir -p $d
  desc="Handles task family $i: formats, checks and reports on files of kind $i. Use when the user asks about kind-$i files."
  if [ $i = 07 ]; then
    desc="$desc"; for n in $(seq 1 40); do desc="$desc Also use for variant $n of kind-07 work, including edge case $n, legacy format $n and any request that mentions kind-07 reports, kind-07 summaries or kind-07 checks in passing."; done
  fi
  { printf -- '---\nname: skill-%s\ndescription: %s\n---\n\n# Skill %s\n\n' $i "$desc" $i
    for n in $(seq 1 15); do echo "$n. Step $n for kind-$i files: read the file, check field $n, write the result."; done
    if [ $i = 03 ]; then echo; echo '```python'; for n in $(seq 1 120); do echo "value_$n = transform(record['field_$n'], mode='strict', fallback=None)  # field $n"; done; echo '```'; fi
    if [ $i = 05 ]; then echo; echo "See [reference.md](reference.md) for field formats."; fi
  } > $d/SKILL.md
done
for i in 05 11; do for n in $(seq 1 60); do echo "- Field $n of kind-$i: a string of up to $n characters, validated by rule $n."; done > $B/skills/skill-$i/reference.md; done
