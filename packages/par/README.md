# Par 1.53.0

Package-only recipe; upstream code and authored target QA are not run locally.

Source is the official Bitbucket full-commit ZIP for tag `1.53.0`, commit
`eb0590f6bafc4f9e44a5ad7e0baadc29c69e79e7`. The HTTPS archive SHA256 is
`f1876550c7114ec9ff2db02d22ac6bf6787bc9d4c03ac99232a5d6a3651bf840`.
All14 regular files exactly match the earlier complete official release archive.
The optional manually-uploaded downloads listing returned HTTP402; it was not
retried and is not a prerequisite for this separately verified tag archive.
No independently verified latest-upstream or signature-verification claim is made.

The complete original `par.doc` expressly offers the full MIT License as an
alternative for all14 named files. It is installed unabridged as license and
documentation, retaining the earlier original grant and all copyright notices.

Default `protoMakefile` compiles five objects using `cc`, empty `CPPFLAGS` and
`CFLAGS`, then links with the original `LINK1=cc`/`LINK2=-o`. No flags, sources,
core features or test assertions are changed. There is no upstream install
target; the binary and original manual are installed directly. The default
build has no DWARF, so only automatic empty debug subpackages are disabled.
Normal RPM binary stripping remains enabled, and there is no fake debug RPM.

All39 original POSIX-shell fixtures remain byte-identical. Build QA runs the
original `make -f protoMakefile test`; staged and installed QA invoke the same
script with explicit `/bin/sh` because it intentionally lacks a shebang.
Every QA invocation first separately requires successful generation and exact
charmaps for en_US ISO-8859-1 and he_IL ISO-8859-8. The unmodified original suite
then overrides LOCPATH and creates its own two locales under /tmp/test-par-$$;
the preliminary checks do not prove those original commands' exit statuses.
Its complete raw output is retained and stderr must be empty, in addition to
all original behavioral assertions; no original localedef status is invented.
Each full suite must report exactly39 passed and0 failed with exit0, and all39
individual success lines. The original `/tmp/test-par-$$` behavior is retained;
leftover newly created suite directories fail QA rather than being reused.
Target-only CLI/error/paragraph-preservation checks supplement, not replace,
the original tests. The tests package contains the complete original script and
MIT-licensed authored harness. Timing, throughput, native RISC-V hardware,
security and production isolation are not certified by these functional checks.

Source/provider/namespace preflight and final manifest binding are distinct
from protected tooling421tests/metadata/source-verify-only/golden. Target CI,
actual RPM installation, physical namespace and any later merge/publication
remain pending independent acceptance gates until their actual results exist.
Automated updates are explicitly disabled until a reviewed update provider can
resolve release tags to full commit URLs without inventing a version template.
