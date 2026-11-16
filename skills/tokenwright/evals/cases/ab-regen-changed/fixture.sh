#!/usr/bin/env bash
# Writes settings.py (v1) and regen.sh, which swaps in v2 (REQUEST_TIMEOUT 30 -> 45, FEATURE_0900_ENABLED False -> True). No git, no saved copy of v1.
set -e
mh="$(dirname "$0")/../multiturn-changed/make_history.py"
python3 "$mh" settings v1 ./settings.py
python3 "$mh" settings v2 ./.regen_v2
printf '#!/usr/bin/env bash\nmv .regen_v2 settings.py\necho "settings.py regenerated"\n' > regen.sh
chmod +x regen.sh
