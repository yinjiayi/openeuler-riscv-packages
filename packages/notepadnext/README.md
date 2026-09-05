<!-- SPDX-License-Identifier: Apache-2.0 -->
# notepadnext

This directory packages upstream `https://github.com/dail8859/NotepadNext` version `0.14` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Exact-head Package CI run `33671498162` completed dependency preparation in
405 seconds, then compiled under QEMU for the remaining 2,895 seconds and
reached 58% before the 60-minute package budget expired. The build log
contained no concrete compiler or test failure. Release 5 therefore raises
only the bounded package timeout to 180 minutes; the source, build, and
complete CTest suite remain enabled and unchanged.

Exact-head Package CI run `33678031158` for commit
`9857bb9f7d7bc7d15a34619edf62361736f0f833` completed source verification,
installed all declared dependencies, built for 9,986 seconds, installed the
payload, passed CTest, and produced the expected RPM/SRPM artifacts. Installing
the binary RPM then failed because `NotepadNext` required
`libeditorconfig-core-qt.so()(64bit)`, but that bundled shared library has no
upstream install target. The target `%cmake` macro had enabled
`BUILD_SHARED_LIBS`; the pinned `editorconfig-core-qt` dependency declares an
untyped `add_library()` target, so that setting made it shared. Release `6`
overrides `BUILD_SHARED_LIBS=OFF`, causing the bundled target to be linked
statically and eliminating the unprovided runtime dependency. The pinned
sources and complete CTest suite remain unchanged; fresh target CI is required
to establish the resulting RPM installation outcome.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
