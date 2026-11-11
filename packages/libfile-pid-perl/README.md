# libfile-pid-perl

File::Pid 1.01 is packaged from the official CPAN archive listed in `sources.yaml`; its SHA-256 matches the publisher's CHECKSUMS. The upstream README grants the same terms as Perl. The frozen Ubuntu lineage is `libfile-pid-perl` 1.01-3.

The original test suite remains enabled. Its fixed temporary filenames are isolated under the build directory. Build and runtime require `perl(Class::Accessor::Fast)` >= 0.19. The target build and installed RPM smoke are verified by exact-head CI, not by local RPM or QEMU builds.
