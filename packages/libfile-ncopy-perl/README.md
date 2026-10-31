# libfile-ncopy-perl

File::NCopy 0.36 is packaged from the official CPAN archive pinned in `sources.yaml`; its SHA-256 matches publisher CHECKSUMS, and its module POD grants Perl terms. The frozen Ubuntu lineage is 0.36-3. Upstream marks this compatibility module deprecated.

All original tests remain enabled. A private seeded temporary directory isolates the upstream copy test, and Test::Pod is installed to exercise its POD test. Exact-head target CI must establish the build and installed RPM smoke; no local RPM or QEMU build is used.
