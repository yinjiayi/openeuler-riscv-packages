# libcidr 1.2.3

The frozen inventory's exact `libcidr` key maps to Matthew D. Fuller's
[official stable release page](https://www.over-yonder.net/~fullermd/projects/libcidr).
The official HTTPS tarball is pinned at SHA-256
`afbe266a9839775a21091b0e44daaf890a46ea4c2d3f5126b3048d82b9bfbbc4`.
Archive inspection found one expected source root, no absolute or parent paths,
and no unsafe links. Distribution and AUR recipes were not executed.

The library is BSD-2-Clause. Its bundled `tools/lorder` build helper has
BSD-4-Clause-UC terms; the helper is used during the build and is not installed.
The SPDX license expression covers both source components.

Upstream provides seven C test programs. `%check` builds all seven and runs
the full registered `src/test/regression/arr.pl` case set through `test.pl`.
Upstream's script reports case failures but exits zero; the package-local patch
changes only failure propagation and test-directory handling. Building the six
other helpers does not claim that their unregistered interactive commands were
fully exercised. Installed smoke independently compiles against the public C
header, checks IPv4 and IPv6 operations, and runs `cidrcalc`.

Target: openEuler 24.03 LTS SP3, `riscv64`, RVA23. CI may fetch the pinned
source over HTTPS and must verify its full SHA-256 before building. A green PR
build is build evidence, not evidence that RPM/SRPM files were publicly
published; their repository URLs must come from a verified publication run.
