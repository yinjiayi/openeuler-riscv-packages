# Bstrlib 1.0.0

Official v1.0.0 resolves to `2529065f2e9fc64aa4ed34df2df4bf0bde718889`;
the fixed archive SHA-256 is
`74396b3273ec4e8972b4cad533c28170534424b1d0c6df44f7875db92b8115c0`.
All 21 original Git files and modes are verified. There is no upstream build
system or source patch. Discovery is the bundled library in
[Debian UEFITool](https://sources.debian.org/src/uefitool/0.28.0%2BA71-1/common/meson.build),
not a standalone Debian package or target-build evidence.

Select the BSD option explicitly documented in bstrlib.txt, retaining the
complete root BSD-3-Clause LICENSE and all original source notices.
Compile every C module, the C++ wrapper with default STL/iostream/exceptions,
and bsafe. The latter deliberately overrides unsafe C functions and is a
separate opt-in static archive; it is not injected into the main library.

Preserve the complete original suites: core test0–48, auxiliary test0–14 and
C++ test0–33 including the STL case. Their mains return zero regardless of
counted failures, so every run must also emit the exact final zero-failure
line. Replay the unmodified test sources against staged and installed public
headers/archives. Do not filter tests or disable features. Real RISC-V build,
installation and physical RPM/SRPM acceptance are separate CI gates; no local
upstream compilation or target execution is performed.
