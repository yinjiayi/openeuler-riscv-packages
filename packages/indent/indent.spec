# SPDX-License-Identifier: Apache-2.0
Name:           indent
Version:        2.2.13
Release:        3%{?dist}
Summary:        C source code formatter
License:        GPL-3.0-or-later AND BSD-3-Clause AND BSD-4.3TAHOE AND Latex2e-translated-notice
URL:            https://www.gnu.org/software/indent/
Source0:        indent-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  texinfo

%description
GNU indent reformats C source code according to configurable coding styles.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_docdir}/%{name}/indent.html
%{_bindir}/indent
%{_infodir}/indent.info*
%{_mandir}/man1/indent.1*

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.13-3
- Accept the documented EX_USAGE status from the informational version option.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.13-2
- Align the installed smoke assertion with GNU-style procedure-name line breaks.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.13-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
