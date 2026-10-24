# SPDX-License-Identifier: Apache-2.0
Name:           alternatives
Version:        1.33
Release:        1%{?dist}
Summary:        Fedora's tool to maintain symbolic links determining default commands.
License:        GPL-2.0-or-later
URL:            https://github.com/fedora-sysv/chkconfig
Source0:        alternatives-1.33.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Fedora's tool to maintain symbolic links determining default commands.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.33-1
- Initial openEuler RISC-V package from the full package inventory.
