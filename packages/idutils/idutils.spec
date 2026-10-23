# SPDX-License-Identifier: Apache-2.0
Name:           idutils
Version:        4.6
Release:        1%{?dist}
Summary:        A package of language independent tools that indexes program identifiers, literal numbers, or words of human-readable text
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/idutils/
Source0:        idutils-4.6.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  hostname


%description
A package of language independent tools that indexes program identifiers, literal numbers, or words of human-readable text

%prep
%autosetup -p1
# This bundled old gnulib assumes gets(3) remains declared by libc.
sed -i '/gets is a security hole - use fgets instead/d' lib/stdio.in.h

%build
%configure
%make_build

%install
%make_install
%find_lang %{name}
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_datadir}/id-lang.map
%{_infodir}/idutils.info*
%{_mandir}/man1/*.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-1
- Initial openEuler RISC-V package from the full package inventory.
