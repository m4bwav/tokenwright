---
type: regex
target: { source: file, path: report.csv }
flags: m
pattern: '^run,warnings,top_warning,failed_tests,slowest_probe\r?$'
---
