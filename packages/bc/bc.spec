# SPDX-License-Identifier: Apache-2.0
Name:           bc
Version:        1.08.2
Release:        1%{?dist}
Summary:        GNU arbitrary precision calculator language
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/bc/
Source0:        bc-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  ed
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  texinfo

%description
GNU bc is an arbitrary precision calculator language. The package also
contains dc, a reverse-polish arbitrary precision calculator.

%prep
%autosetup -p1

%build
%configure --with-readline
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check
printf '2 + 2\n' | ./bc/bc | grep -qx '4'
printf '2 3 + p\n' | ./dc/dc | grep -qx '5'
printf 'scale=10; sqrt(2)\n' | ./bc/bc -l | grep -qx '1.4142135623'

%files
%license COPYING COPYING.LIB
%doc AUTHORS FAQ NEWS README Examples
%{_bindir}/bc
%{_bindir}/dc
%{_mandir}/man1/bc.1*
%{_mandir}/man1/dc.1*
%{_infodir}/bc.info*
%{_infodir}/dc.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.08.2-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
