# SPDX-License-Identifier: Apache-2.0
Name:           ddccontrol
Version:        1.0.3
Release:        1%{?dist}
Summary:        DDCcontrol is a software used to control monitor parameters, like brightness, contrast, RGB color levels and others
License:        GPL-2.0-or-later
URL:            https://github.com/ddccontrol/ddccontrol
Source0:        ddccontrol-1.0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
DDCcontrol is a software used to control monitor parameters, like brightness, contrast, RGB color levels and others

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
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
