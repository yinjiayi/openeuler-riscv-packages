<!-- SPDX-License-Identifier: Apache-2.0 -->
# awf-gtk2

This directory packages upstream `https://github.com/luigifab/awf-extended` version `4.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned tag archive expands beneath `awf-extended-4.2.0`. The RPM build runs upstream's Autotools configuration in GTK 2-only mode and declares the compiler, gettext, pkg-config, GTK 2, and libnotify development dependencies required by that configuration.

The English and French manual pages are listed separately from the generated file manifest so RPM's post-install compression cannot leave stale uncompressed paths in the package file list.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
