# SPDX-License-Identifier: Apache-2.0
Name:           libverto
Version:        0.3.2
Release:        1%{?dist}
Summary:        Main event loop abstraction library
License:        MIT
URL:            https://github.com/latchset/libverto
Source0:        libverto-0.3.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Main event loop abstraction library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
