<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpeas

This directory packages GNOME libpeas `1.36.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It supplies the `pkgconfig(libpeas-1.0)` and `pkgconfig(libpeas-gtk-1.0)` development interfaces required by consumers such as `xed`.

The source is the official GNOME `libpeas-1.36.0.tar.xz` release. Its SHA-256 matches GNOME's adjacent checksum file and the byte-identical archive in openEuler's `openEuler-24.03-LTS-SP3` dist-git commit `f13e7a350c17d893986ce6ff23e3a33ebd639f8a`. The current openEuler EPOL RVA23 repository independently publishes `libpeas` and `libpeas-devel` `1.36.0-1.oe2403sp3`; its devel RPM advertises both required pkg-config capabilities.

The package retains openEuler's GTK 3, GObject introspection, Python 3 loader, Glade catalog, and generated documentation feature set. Unlike the distribution SPEC, `%check` runs every Meson-registered core, Python, and GTK test through Xvfb, matching upstream's official headless GTK CI procedure. Demos remain disabled as in the openEuler package and are not part of the installed libraries or test contract.

The fixed target repository snapshot provides every declared build dependency. No local RPM/QEMU build or repository publication was performed, so the RISC-V status remains `unknown` and no RPM or SRPM availability is claimed.

External source licenses remain those of the upstream project. The repository license only covers original packaging metadata, scripts, and documentation.
