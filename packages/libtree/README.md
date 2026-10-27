# libtree

This package selects Harmen Stoppels’ ELF dependency-tree CLI, not Piumarta’s
unrelated same-name AVL library. The actual official non-prerelease v3.1.1
release, source VERSION and CHANGELOG agree. Source0 pins commit
`1521dfe063284551b955958fd7deb3426fd75d84`; the archive SHA-256 is
`07fa7a3f151f4c8264a5402697c2ffb5e9be577eb66dc92cbb2759cfefbc05fd`.
All 24 Git blobs and modes match. The observed tag and commit are unsigned;
API metadata and release checksums for other-architecture binaries are not
independent source signatures. No prebuilt binary is used.

Original all builds the C99 CLI; original install supplies the CLI and man1.
There is no CMake build or public library ABI here. All nine original test
directories, 21 CLI invocations (16 positive and five shell-negated), options,
default search paths and warnings are retained. Root MIT LICENSE and every
original file, including documentation/screenshot and fixture Makefiles, ship
unchanged as 24 SHA-256-bound source notices before either patch is applied.
Original packaging/added QA is Apache-2.0 with the complete text shipped too.

Patch1 exposes original -m32/-m64 test flags without changing their defaults.
Only target CI’s four original `-nostdlib` parser-data files use rv32imac/ilp32
or rv64imac/lp64 flags. **Inert test data** means those generated ELF files are
opened and parsed by libtree, never executed, installed or shipped as a 32-bit
runtime/RPM. No 32-bit libc is required. The actual binary remains built with
normal RPM riscv64/RVA23 flags. GCC/ld ability is unproven until target CI;
readelf class/machine/dependency records must confirm all four original files.
Patch2 fixes narrow loop progress/array-capacity handling for long dependency
names/search components. This is static source reasoning, not an observed
crash, CVE, proof of complete malformed-ELF safety, or native-loader fidelity.
Both patches state provenance/removal conditions and preserve upstream notices.

Six additive deterministic CLI groups check version; precise malformed-header
errors; ELF32/64 parser data; dependency class/machine compatibility; original
RPATH/environment/RUNPATH order; and long-needed/search-component boundaries.
The owned Python generator writes read-only synthetic ELF *data*, not executable
code and not replacements for the nine original compiler-fixture suites. Only
libtree runs, under bounded per-command timeouts. All 12 invocation stdout/stderr/status contracts are exact. Self/program SHA-256
and resolved paths/cwd/relevant environment are recorded, and all 20 data files
plus complete command streams are emitted on success or failure. Installed smoke verifies final post-strip
binary/helper hashes, all24 notices and ELF64/RISC-V/no-RPATH before repeating
all six groups against the actual /usr/bin/libtree. No host build, source test,
native benchmark, network feature test or target acceptance is claimed here.

Discovery uses the retained frozen catalog rows30295/131606; raw opensuse/oss
maps explicitly to schema opensuse-tumbleweed. URL-null89098 and unrelated
Piumarta173060 remain distinct evidence, not official release authority. Source
capture/rights review, fresh full semantic/namespace/provider admission, trusted
repository gates and target CI remain separate gates. Ordinary GitHub release
tracking is enabled, without an unsupported full Daily coverage claim.
