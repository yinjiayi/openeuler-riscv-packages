# SPDX-License-Identifier: Apache-2.0
Name:           scim
Version:        1.4.18
Release:        1%{?dist}
Summary:        Input method user interface and development platform
License:        LGPL-2.1-or-later
URL:            https://github.com/scim-im/scim
Source0:        scim-1.4.18.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Input method user interface and development platform

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.18-1
- Initial openEuler RISC-V package from the full package inventory.
