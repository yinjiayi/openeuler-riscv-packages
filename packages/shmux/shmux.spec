# SPDX-License-Identifier: Apache-2.0
Name:           shmux
Version:        1.0.3
Release:        2%{?dist}
Summary:        shmux - executing the same command on many hosts in parallel.
License:        BSD-3-Clause
URL:            https://github.com/shmux/shmux
Source0:        shmux-1.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pcre-devel

%description
shmux - executing the same command on many hosts in parallel.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-2
- Declare terminal and PCRE development dependencies and run the upstream test target.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
