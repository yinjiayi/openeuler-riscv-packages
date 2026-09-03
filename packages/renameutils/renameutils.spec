# SPDX-License-Identifier: Apache-2.0
Name:           renameutils
Version:        0.12.0
Release:        1%{?dist}
Summary:        Utilities for renaming files more efficiently
License:        GPL-3.0-or-later
URL:            https://www.nongnu.org/renameutils/
Source0:        renameutils-%{version}.tar.gz
Patch0:         0001-build-fix-bindir-expansion.patch

BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  readline-devel

%description
renameutils is a set of command-line utilities for renaming and copying files
with editable name lists or GNU Readline support.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
%find_lang %{name} --all-name

%check
%make_build check
for command in qcmd qmv qcp icmd imv icp deurlname; do
  "./src/$command" --version >/dev/null
done

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/qcmd
%{_bindir}/qmv
%{_bindir}/qcp
%{_bindir}/icmd
%{_bindir}/imv
%{_bindir}/icp
%{_bindir}/deurlname
%{_mandir}/man1/qcmd.1*
%{_mandir}/man1/qmv.1*
%{_mandir}/man1/qcp.1*
%{_mandir}/man1/icmd.1*
%{_mandir}/man1/imv.1*
%{_mandir}/man1/icp.1*
%{_mandir}/man1/deurlname.1*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-1
- Initial package from the official Savannah 0.12.0 release archive.
- Preserve the complete utility and translation set with the upstream check gate.
- Fix the upstream bindir expansion so staged installation succeeds.
- Include the bundled gnulib message catalogs in the RPM language manifest.
