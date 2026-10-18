# libfixmath

The fixed upstream commit is byte/mode-identical to all 59 source files in
Debian's 20220222 orig archive; Debian's embedded Git metadata is not packaged.
The RPM version denotes that reviewed snapshot, not an upstream tagged release.

The unmodified CMake build retains all twelve UBSan-instrumented CTest variants.
The original runner invokes eight test groups; its already-commented string test
is not claimed as tested. Staged and installed smoke checks compile those same
original tests against the actual default-configuration archive. They do not
claim to validate the other eleven variants as installed ABIs. No timing or
performance benchmarks run. MIT and the original public-domain FFT notice are
both retained. Local validation executes repository tooling only.
