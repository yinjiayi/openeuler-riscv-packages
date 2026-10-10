# SPDX-License-Identifier: Apache-2.0
Name:           stress
Version:        1.0.7
Release:        1%{?dist}
Summary:        A tool that stress tests your system (CPU, memory, I/O, disks)
License:        GPL-2.0-or-later
URL:            https://github.com/resurrecting-open-source-projects/stress
Source0:        stress-1.0.7.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool that stress tests your system (CPU, memory, I/O, disks)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Initial openEuler RISC-V package from the full package inventory.
