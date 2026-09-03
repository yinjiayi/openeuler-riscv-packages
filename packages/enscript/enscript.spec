# SPDX-License-Identifier: Apache-2.0
Name:           enscript
Version:        1.6.6
Release:        1%{?dist}
Summary:        Convert text files to PostScript and other formats
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/enscript/
Source0:        enscript-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make

%description
GNU Enscript converts text files to PostScript, HTML, RTF, ANSI, and
overstrikes, with syntax highlighting and configurable output layouts.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%find_lang enscript

%check
%make_build check

%files -f enscript.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/enscript.cfg
%{_bindir}/diffpp
%{_bindir}/enscript
%{_bindir}/mkafmmap
%{_bindir}/over
%{_bindir}/sliceprint
%{_bindir}/states
%{_datadir}/enscript/
%{_infodir}/enscript.info*
%{_mandir}/man1/diffpp.1*
%{_mandir}/man1/enscript.1*
%{_mandir}/man1/sliceprint.1*
%{_mandir}/man1/states.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.6-1
- Initial openEuler RISC-V package from the full package inventory.
