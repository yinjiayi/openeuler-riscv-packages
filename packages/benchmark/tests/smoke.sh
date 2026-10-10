#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- benchmark benchmark-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <benchmark/benchmark.h>

static void BM_InstalledLibrary(benchmark::State& state) {
  for (auto _ : state) benchmark::DoNotOptimize(42);
}

BENCHMARK(BM_InstalledLibrary);
BENCHMARK_MAIN();
CPP
g++ -std=c++14 "$task_dir/smoke.cpp" -lbenchmark -lpthread -o "$task_dir/smoke"
"$task_dir/smoke" \
  --benchmark_filter=BM_InstalledLibrary \
  --benchmark_min_time=0.001s \
  --benchmark_repetitions=1
