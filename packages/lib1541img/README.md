# lib1541img

Official stable v1.1 pins `excess-c64/lib1541img` commit
`a747810f0c46d49d37711e3bade1c5c85a4b261d`. Its required `zimk` build submodule
is the exact gitlink `Zirias/zimk@31500ca556f258ab2d37d75fb8de5506cbdd5840`,
not a floating tip. Both official archives have independent SHA-256 checksums
in sources.yaml. All62 parent Git files and19 child files were inspected
inertly against official Git blobs. Both original BSD-2-Clause notices are
retained in the SRPM and runtime license payload. No source patch is applied.

Historical AUR snapshot `discovery-20260808T165000Z-9a89920c269462cd` recorded
lib1541img1.1-1 as stale. That is discovery lineage, not recipe/source authority
or a current eligibility decision. Fresh official tag, complete source and
license checks supersede stale-only selection; no AUR recipe was executed.

The recipe preserves upstream's complete default `make all` shared build.
Upstream declares no check/test target or original functional test program.
An empty/default build is not called a functional suite. Optional staticlibs
and Doxygen html targets are not defaults; no feature is patched out. RPM
owns stripping/debug splitting. The library/pkg-config ABI version is1.1.0,
while the official release and RPM version are1.1.

Separately labeled downstream consumers check every track/sector's geometry,
coordinates and zero initialization; all35/40/42-track exact image sizes;
D64 write/read with full-sector byte preservation; invalid coordinates and
constructors; and uppercase PETSCII/UTF8 conversion. They run against source,
staged headers/library/pkg-config and installed RPM-owned products. Explicit
failures are independent of NDEBUG. Installed smoke also checks RPM integrity,
pkg-config paths and loader ownership. These are not fabricated upstream tests.

Full official18503 and M34 supplemental1228 binary primary/filelists were
joined by checksum/name/arch/EVR. No name/provide/require/header/library/
pkg-config collision was found, nor in managed metadata or1843 exact open
heads. GCC14.3.1, GNU make4.4.1, binutils2.42, glibc2.38, pkgconf1.9.5 and
declared base tools are supplied. Dependency closure has no absent name;
literal EVR bounds and the versionless libxcrypt-static capability remain
explicit in the witness, not silently treated as a versioned provide. The
actual DNF transaction and this offline recipe remain exact-head CI gates.

No local source, RPM or QEMU build was run. Hosted PR CI must prove the locked
openEuler24.03-LTS-SP3/riscv64/RVA23 target. Native hardware, merge and public
release are separate gates. Other candidates' missing frameworks and a
Dashboard API outage do not freeze independent safe hosted PR intake.
