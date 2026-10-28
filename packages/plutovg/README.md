# PlutoVG 1.3.3 static SDK

The official fixed archive is SHA256 f9bb31ff305381b79bb920730017bd356e5043a215960dd83656c70036075a4e,
commit bbd91f0d06a71491691b36330f29dffa4af87ccf, all35 Git files exact.
This proposal preserves native CMake static output and the original enabled
smiley example; it neither changes upstream source nor disables font-cache loading.
There is no registered original test suite in the complete fixed tree. The
original smiley is built and executed, then its PNG is decoded with CRC, size,
alpha and interior-pixel checks. This is example coverage, not an invented suite.

Owned two-translation-unit consumers validate seven semantic groups, including
matrix/path/color/raster/Unicode and real font metrics, glyph/text drawing,
cache add/reset and file/directory loading. C99/C11 use both exact CMake exported
target and pkgconf --static, at installed and relocated SDK prefixes (8 routes
per phase). Exact archive/header/link-map/ELF and all11 AR-object provenance,
plus missing-header and missing-library negatives, prevent ambient SDK success.
The DejaVuSans input is not redistributed: its actual official package NEVRA,
RPM SHA256 and exact font digest are pinned in the installed QA contract.

All35 original source files are rehashed through prep/build/install/check and
retained byte-for-byte as source notices. LICENSE and FTL.TXT are copied as raw
bytes, including FTL's legacy copyright byte; they are never transcoded from
replacement-glyph JSON text. The seven FT-derived files use FTL; the three STB
headers use their explicit MIT alternative A while preserving both offered
alternatives and embedded attributions. Binary documentation credits the
FreeType Team and reports no upstream source modifications. Apache2 applies
only to owned packaging/QA. These are component grant scopes, not a blanket MIT
claim, personal warranty or separate permission from individual contributors.

Only the static archive/header/pc/CMake exports plus QA/docs/licenses are
installed. No production CLI or shared library is claimed. Automatic debug
subpackages are disabled because no executable/DSO is installed; this says
nothing about whether static archive objects contain DWARF.

This is an inert proposal. Formal root rights/source/provider admission, trusted
factory preview/create and local metadata/test/golden checks precede a PR;
actual RVA23/QEMU-user build and installed validation remain unobserved here.
