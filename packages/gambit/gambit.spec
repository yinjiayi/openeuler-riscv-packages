# SPDX-License-Identifier: Apache-2.0
Name:           gambit
Version:        16.7.0
Release:        2%{?dist}
Summary:        Tools for doing computation in game theory
License:        GPL-2.0-or-later
URL:            https://github.com/gambitproject/gambit
Source0:        gambit-16.7.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Tools for doing computation in game theory

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
%license license.rtf
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 16.7.0-2
- Raise the bounded QEMU build timeout to 180 minutes after exact-head CI
  compiled normally until the 60-minute package budget expired.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 16.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
