# Picocom 3.1

Official Arch extra 3.1-3 delegates `npat-efault/picocom`. Official stable tag
`3.1` resolves to commit `90385aabe2b51f39fa130627d46b377569f82d4a`.
The fixed official archive is SHA-256
`a38f431d27b6c6275b0c281c7d53f0bfc7bf22d251122d53a56fb407457e2054`.
Its 40 regular files are joined to the complete Git tree and original modes.
The captured release has no assets/signature links and its annotated tag is
unsigned; this records the reviewed official surface, not universal absence.

Keep the original `make all` seven-object build, including vendored linenoise,
history, help, HIGH_BAUD, USE_FLOCK and the unlimited TTY queue. No feature
defines are removed or forced. Upstream enables Linux custom-baud handling by
default only on selected architectures (not RISC-V); preserve that selection.
Do not interpret a PTY check as custom-baud or physical UART/modem verification.

There is no upstream install target: README directs copying the built binary
and pregenerated `picocom.1`. Install those unchanged; leave stripping to the
standard RPM debug machinery. Non-default documentation regeneration requires
pandoc/groff and private user templates, so use the shipped man/HTML/PDF instead
of running that non-default target. All original docs, contributors and four
helper scripts are documentation; no new helper commands are installed under
`/usr/bin`. The entire fixed source archive, including all helpers and vendor
notices, is retained in the tests package. Core/manual GPL2-or-later and full
linenoise BSD2-clause texts are included in both binary packages.

Default send/receive commands stay `sz -vv` and `rz -vv -E`; `lrzsz` must supply
their actual installed commands. No file-transfer feature is disabled. External
helper examples have additional command dependencies, documented by their
unchanged source; shipping examples is not a claim to test those protocols.

Upstream root and vendor Makefiles have no automated test/check target. Newly
authored downstream QA verifies installed files/notices/source and help/default
features, negative CLI cases, init-string immediate exit, and bidirectional
binary PTY transfer with logging and explicit CR/LF maps. It uses private HOME,
two private PTYs, bounded waits and isolated child process groups, never real
serial devices. `%check` and installed smoke execute this on the target only.
No local upstream, authored QA, compiler, RPM or QEMU execution was performed;
metadata, repository tests, target QA and physical artifacts are separate gates.
