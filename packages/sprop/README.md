# Sprop 0.1

Canonical component: `tools.suckless.org-sprop`; official stable release
https://dl.suckless.org/tools/sprop-0.1.tar.gz, SHA-256
`c1b786d9fbd81a57addd7e21a34c5a121543cbf9f38fe309e7b452ba94b69ab5`.
All six original source members were reviewed. MIT/X Consortium notice (2010
Connor Lane Smith) is installed unchanged. No patch, bundled library or image.

Fresh distribution discovery: Debian trixie stable `suckless-tools` source
48-1 lists its separate orig-sprop source and the sprop binary/manpage/README.
https://packages.debian.org/trixie/suckless-tools
https://packages.debian.org/trixie/amd64/suckless-tools/filelist
This is explicit bundled-component lineage only: 48-1 is the Debian bundle's
version, not upstream sprop's 0.1, not a source alias, and no frozen-catalog row
is invented. The independently downloaded official archive defines this recipe.

Preserve original default all/options/install targets and C99/pedantic/Wall,
VERSION, libc and Xlib behavior. Distribution compiler/debug/optimization/link
flags and /usr installation prefix replace only local build settings. Upstream
has no test/check target. Mandatory downstream QA, never optional: one private
bounded Xvfb, no DISPLAY negative, exact version/usage, pre-created UTF8 atoms,
decimal XID, independent Xlib get/set/type/format/byte proof, empty/ASCII/space/
UTF8/multiline/8192-byte values, cleanup. Run built and staged QA in %check and
installed QA in committed smoke. README/LICENSE/manpage integrity is checked.

Target: locked openEuler24.03 LTS SP3 riscv64 RVA23 QEMU-user profile; offline
unprivileged build. gcc/make/libX11-devel/pkgconfig and Python/Xvfb provide build
and semantic test dependencies; runtime Xlib is automatically required. Tests
subpackage requires the exact package EVR, Python, Xlib, Xvfb and Bash. No X
server or dependency is embedded. No local upstream/target execution; repository
tooling/source verification is not target build/install or native acceptance.
Physical products, exact-head CI and complete namespace acceptance remain
mandatory before explicit protected squash. Auto-merge is not enabled.
