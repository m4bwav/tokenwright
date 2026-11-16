Triage the CI runs in runs/, one run at a time, starting with run-01. For each run:
1. build.log: count the WARN lines and find the most frequent warning code (the W-number in brackets).
2. tests.log: count the failed tests.
3. probes.log: find the endpoint of the probe with the highest latency.

Write report.csv in this folder with the header `run,warnings,top_warning,failed_tests,slowest_probe` and one row per run, then tell me which run looks worst.
