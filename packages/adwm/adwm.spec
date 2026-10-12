# SPDX-License-Identifier: Apache-2.0
Name:           adwm
Version:        0.7.17
Release:        1%{?dist}
Summary:        Advanced dynamic window manager for X
License:        MIT
URL:            https://github.com/bbidulock/adwm
Source0:        adwm-0.7.17.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Advanced dynamic window manager for X

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
%license LICENSE
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.17-1
- Initial openEuler RISC-V package from the full package inventory.
