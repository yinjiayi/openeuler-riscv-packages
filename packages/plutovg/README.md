# PlutoVG 1.3.3 static SDK

The official fixed archive is SHA256 f9bb31ff305381b79bb920730017bd356e5043a215960dd83656c70036075a4e,
commit bbd91f0d06a71491691b36330f29dffa4af87ccf, all35 Git files exact.
This proposal preserves native CMake static output and the original enabled
smiley example and font-cache loading. One generic UTF-16 lookahead correction
changes only source/plutovg-font.c; no RISC-V-specific source defect is claimed.
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

All35 original source files are verified before patch application and copied
to a private original snapshot for byte-exact source notices. Later build,
install and check phases verify all35 against an exact post-patch manifest;
only source/plutovg-font.c changes, and the other34 sources are unchanged. LICENSE and FTL.TXT are copied as raw
bytes, including FTL's legacy copyright byte; they are never transcoded from
replacement-glyph JSON text. The seven FT-derived files use FTL; the three STB
headers use their explicit MIT alternative A while preserving both offered
alternatives and embedded attributions. Binary documentation credits the
FreeType Team and identifies the one generic MIT-source modification; the
seven FT-derived files and three STB headers are unchanged. Apache2 applies
only to owned packaging/QA. These are component grant scopes, not a blanket MIT
claim, personal warranty or separate permission from individual contributors.

Only the static archive/header/pc/CMake exports plus QA/docs/licenses are
installed. No production CLI or shared library is claimed. Automatic debug
subpackages are disabled because no executable/DSO is installed; this says
nothing about whether static archive objects contain DWARF.

The first current-head target failed in the unchanged Unicode consumer on
UTF-16 U+1F600 after four semantic groups passed. The leading unit is tested
against D800 and then incorrectly against DC00; the latter predicate must peek
at text[it->index] under the existing length guard. The patch changes that
one expression only. The valid supplementary regression, all seven groups,
eight installed/relocated C99/C11 routes, original example/defaults and font
checks remain unchanged. No upstream write was made: status not-submitted.
Remove this patch when a fixed upstream source contains the equivalent change
and full replacement build/install/physical gates pass. Invalid-surrogate
semantics, native-only behavior and target success are not claimed.

The same-PR repair requires an exact-head lease, reviewed package-only changes,
trusted repository validation and a normal guarded push. Replacement target,
installed validation and physical acceptance remain pending; earlier failures
and the cumulative attempt budget remain recorded.
