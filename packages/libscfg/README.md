# libscfg 0.2.0

The frozen inventory's exact `libscfg` key maps to the official Codeberg
project `emersion/libscfg`. The upstream `v0.2.0` annotated tag resolves to
commit `f7d74ce6c81e55976d85b824ba73c03f6c0f157a`. The official HTTPS
tag archive has SHA-256
`cf37ef00ac8efb28821dac1ad49e2c6b23b242d9d961fab6fcda72fc73a7291b`.
Its 13 archive members contain no unsafe paths or links. The upstream license
is MIT; the source archive contains its `LICENSE` text.

The Meson build installs the shared library, public C header, and pkg-config
file. `%check` runs the entire upstream-registered test set: the `parse` and
`format` cases. Both test branches return a nonzero exit code on failure.
The installed smoke check separately compiles an external C client with
pkg-config, parses a directive, and checks the resulting public data model.
The first CI run (`36494388501`) passed both tests but failed RPM's file-list
check: the SPEC included the `.so.2` SONAME but omitted the real
`libscfg.so.0.2.0` file. Both paths are now listed; a new exact-head CI run
must still verify the corrected package and installed smoke.

This PR's target is openEuler 24.03 LTS SP3, `riscv64`, RVA23 under the CI
QEMU-user profile. A successful PR CI build yields CI artifacts; it is not
proof that the RPM/SRPM files were published to the public repository.
