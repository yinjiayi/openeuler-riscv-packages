# SPDX-License-Identifier: Apache-2.0
Name:           units
Version:        2.27
Release:        1%{?dist}
Summary:        Convert quantities between systems of measurement
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/units/units.html
Source0:        units-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  readline-devel
Requires:       python3

%description
GNU Units converts quantities between thousands of measurement systems and
supports compound units, nonlinear conversions, and currency data updates.

%prep
%autosetup -p1

%build
%configure --sharedstatedir=%{_localstatedir}/lib
%make_build

%install
%make_install

%check
%make_build check
result=$(./units -t -f definitions.units meter centimeter)
test "$result" = "100"

%files
%license COPYING
%doc NEWS README units.txt
%{_bindir}/units
%{_bindir}/units_cur
%{_datadir}/units/
%{_localstatedir}/lib/units/
%{_infodir}/units.info*
%{_mandir}/man1/units.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.27-1
- Initial openEuler RISC-V package from the full package inventory.
