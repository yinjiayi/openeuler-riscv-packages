# libred 1.1.3

Solar elevation and blackbody colour library, fixed official Codeberg archive
with SHA-256 recorded in sources.yaml. ISC copyright/permission notices are
retained in each subpackage. Frozen AUR 1.1.3-1 is discovery lineage only.

The original default `all` builds both libraries, runs the original target-built
table generator and consumes the entire original colour table. It is unchanged.
Upstream has no `check` or `test` target and no upstream test driver; the package
does not claim otherwise. Two original internal manual aliases are preserved in
the original archive and installation. Only the install library directory moves
to the openEuler lib64 convention; no source patch or feature switch is used.

Package-added functional checks compile a consumer against staged and normally
installed shared/static libraries. They verify every table row and intermediate
temperature range, documented lower-bound errors, 6500K calibration, linear xy
interpolation, upper-bound clamping, inverse API linkage and calibration, solar
finite/range output and public twilight macros. Full source archive and public
header bytes are checked. These are bounded packaging/functional ABI checks, not
a complete upstream suite, independent scientific or astronomy accuracy tests,
hardware or clock accuracy, native timing, or performance validation.

Local verification is repository tooling and shell syntax only. Target build,
normal DNF installation, installed smoke and physical RPM/SRPM verification
remain mandatory before protected explicit squash. No local source/RPM/QEMU
build is part of admission.
