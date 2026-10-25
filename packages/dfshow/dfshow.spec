# SPDX-License-Identifier: Apache-2.0
Name:           dfshow
Version:        1.0.1
Release:        1%{?dist}
Summary:        An interactive directory/file browser written for Unix-like systems.
License:        GPL-3.0-or-later
URL:            https://github.com/roberthawdon/dfshow
Source0:        dfshow-1.0.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
An interactive directory/file browser written for Unix-like systems.

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
%license LICENSE
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
