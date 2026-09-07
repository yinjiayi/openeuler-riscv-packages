<!-- SPDX-License-Identifier: Apache-2.0 -->
# libreport

This directory packages upstream `https://github.com/abrt/libreport` version `2.17.15` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build regenerates the Autotools files and therefore declares
`gettext-devel`, which is the target repository package that provides
`/usr/bin/autopoint`. The GitHub tag archive omits the generated
`libreport-version` file, so the build materializes it deterministically from
the RPM version before regeneration. The target `intltool` package supplies
the macro and helper used by `IT_PROG_INTLTOOL`. The build also declares the
`asciidoc` and `xmlto` tools that `configure.ac` requires to generate the
installed documentation. The default-enabled Bugzilla, Python, newt, GTK,
uReport, journal, Augeas, and archive features retain their target development
dependencies, and the complete upstream `make check` suite retains its locale
data.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
