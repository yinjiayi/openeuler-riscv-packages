# libfixmath

The retained arithmetic patch repairs source undefined behavior reported by the
original UBSan variants in run 39126145006. It performs bit assembly, rounding
wrap, and INT32_MIN magnitude conversion as unsigned arithmetic and handles a
zero emulated-64-bit shift without shifting by 32. Source CRLF hunk endings are
preserved. All twelve original CTest variants, original tests, instrumented
configuration and zero-diagnostics gate remain unchanged. A replacement hosted
build is required; local inert patch checks are not a target-build acceptance.

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
