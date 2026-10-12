# SPDX-License-Identifier: Apache-2.0
Name:           intel-lpmd
Version:        0.1.0
Release:        1%{?dist}
Summary:        Intel Low Power Mode Daemon
License:        GPL-2.0-or-later
URL:            https://github.com/intel/intel-lpmd
Source0:        intel-lpmd-0.1.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Intel Low Power Mode Daemon

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
