set -euo pipefail

ERR_FILE="${1:-errors.log}"
PREVIEW_N="${PREVIEW_N:-10}"

if [[ ! -f "$ERR_FILE" ]]; then
  echo "ERROR: errors file not found: $ERR_FILE" >&2
  exit 1
fi

total=$(grep -cve '^[[:space:]]*$' "$ERR_FILE" || true)

echo "Errors file : $ERR_FILE"
echo "Total errors: $total"

if [[ "$total" -eq 0 ]]; then
  exit 0
fi

echo
echo "== Errors by action (top 10) =="
awk -F' \\| ' '
  NF>=1 {
    action=$1
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", action)
    if (action != "") cnt[action]++
  }
  END {
    for (a in cnt) printf "%d\t%s\n", cnt[a], a
  }
' "$ERR_FILE" | sort -nr | head -n 10

echo
echo "== Errors by exception type (top 10) =="
awk -F' \\| ' '
  NF>=3 {
    # 第3段形如: "ValueError: xxx"
    ex=$3
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", ex)
    sub(/:.*/, "", ex)
    if (ex != "") cnt[ex]++
  }
  END {
    for (e in cnt) printf "%d\t%s\n", cnt[e], e
  }
' "$ERR_FILE" | sort -nr | head -n 10

echo
echo "== Last ${PREVIEW_N} errors (raw) =="
tail -n "$PREVIEW_N" "$ERR_FILE"
