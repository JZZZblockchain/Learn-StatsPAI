#!/usr/bin/env bash
# Run the Track C benchmarks once the machine is idle.
#
#   tests/perf/run_when_idle.sh [SRC]
#
# SRC is the statspai source tree to benchmark (default: this checkout's
# src/). It (1) writes the shared inputs (tests/perf/_data.py), (2) pins
# every thread pool to one thread on both sides, (3) waits until the
# 1-minute load average has stayed below $LOAD_MAX (default 1.5) for five
# one-minute samples, and (4) runs the Python and R sides of each module
# under one run id, which compare_perf.py requires both sides to share.
# Wall-clock timings from a busy machine are not comparable: a run under
# load ~9 once inflated ratios by 20-30%.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${1:-$HERE/../../src}"
LOAD_MAX="${LOAD_MAX:-1.5}"
export PYTHONPATH="$SRC"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export STATSPAI_PERF_RUN_ID="${STATSPAI_PERF_RUN_ID:-$(date +%Y%m%dT%H%M%S)}"
PY="${PYTHON:-python3}"
command -v Rscript >/dev/null || { echo "Rscript not found: the reference legs cannot run" >&2; exit 2; }
load1() { if command -v sysctl >/dev/null && sysctl -n vm.loadavg >/dev/null 2>&1; then sysctl -n vm.loadavg | awk '{print $2}'; else awk '{print $1}' /proc/loadavg; fi; }
cd "$HERE"
"$PY" _data.py
streak=0
while (( streak < 5 )); do
  l=$(load1)
  if awk -v l="$l" -v m="$LOAD_MAX" 'BEGIN{exit !(l < m)}'; then streak=$((streak+1)); else streak=0; fi
  (( streak >= 5 )) && break
  echo "$(date +%T) waiting, load=$l"; sleep 60
done
"$PY" -c "import statspai; print('benchmarking statspai', statspai.__version__, 'from', statspai.__file__)"
echo "run id $STATSPAI_PERF_RUN_ID"
for m in 01_hdfe 02_csdid 03_scm; do
  echo "=== $m py $(date +%T) load=$(load1)"; "$PY" "${m}_perf.py"
  echo "=== $m R  $(date +%T) load=$(load1)"; Rscript "${m}_perf.R"
done
echo "=== 04_dml py + doubleml-for-py $(date +%T) load=$(load1)"; "$PY" 04_dml_perf.py
"$PY" compare_perf.py
echo "=== done $(date +%T) load=$(load1)"
