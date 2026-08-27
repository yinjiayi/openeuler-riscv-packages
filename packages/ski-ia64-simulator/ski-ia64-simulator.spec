# SPDX-License-Identifier: Apache-2.0
Name:           ski-ia64-simulator
Version:        1.5.1
Release:        1%{?dist}
Summary:        Itanium 2 (ia64) instruction set simulator
License:        GPL-2.0-or-later
URL:            https://github.com/trofi/ski
Source0:        ski-ia64-simulator-1.5.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Itanium 2 (ia64) instruction set simulator

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
