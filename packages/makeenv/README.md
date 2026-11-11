# Makeenv

Makeenv 1.0.3 loads options, macros and targets from `.makeenv` before
executing make. Fixed official source bytes and the complete ISC notice are
retained in both binary packages and the unchanged QA/SRPM source archive.

The original default build is unchanged. Upstream has no check/test target;
staged/installed argument ordering, environment propagation, real-make execution
and error statuses 125/126/127 are downstream functional checks, not an original
upstream suite. No source patch, local source/RPM/QEMU execution, privileged,
performance or native-host claim. Exact-head required/full CI, ordinary target
installation and physical RPM/SRPM acceptance remain merge gates.

The exact argument comparison preserves upstream's operand order: `.makeenv`
targets precede command-line operands, including command-line macros, which
`put_operand` deliberately stores without reordering. The downstream expected
list follows that contract; all comparisons and error-status checks remain.
