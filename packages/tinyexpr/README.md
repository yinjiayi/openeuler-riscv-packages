# Tinyexpr 1.1.1

Official tag `v1.1.1` resolves to
`6d2233ce14dca063994708a91b3b98e24e8aa0c3`. The complete 20-file archive
is SHA-256 `cdeaf4bbd89d00e70a2423fd96d069918c1d2eeca13c0924c6b3cb91c527603f`.
The implementation, header, smoke and minctest notices retain Lewis Van Winkle's
Zlib terms. No source patch, imported distribution build logic or networked
test dependency is used.

Discovery evidence is the [bundled Tinyexpr component in Debian mmseqs2](https://sources.debian.org/src/mmseqs2/12-113e3%2Bds-3/lib/tinyexpr/),
not a standalone Debian Tinyexpr package or proof of this version's build.
The independently reviewed official stable tag supplies this package's bytes.
Canonical homepage is `https://codeplea.com/tinyexpr`; repository is
`https://github.com/codeplea/tinyexpr`.

Upstream has no install rule. Downstream installs `tinyexpr.h` and a static
archive made from the original default object; consumers link `-ltinyexpr -lm`.
Preserve the complete upstream `make all`: both original smoke modes,
three examples, REPL and benchmark build. The benchmark is never executed;
no timing/performance or native-RISC-V claim is made.

Both smoke modes retain all 15 original groups, including 5000 number-parsing
cases and locale checks. Require the target's German locale provider so the
original locale case cannot silently skip. Re-run both bare binaries in
`%check`, and compile unchanged default smoke sources against staged/installed
header and archive. The test package contains no implementation source.
Only target CI can establish RISC-V build/install success; source-only
verification and repository tooling checks are not target-build evidence.
