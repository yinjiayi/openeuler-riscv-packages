# SPDX-License-Identifier: Apache-2.0
Name:           potato-c
Version:        0.7.4
Release:        1%{?dist}
Summary:        A featureful, modular and fast pomodoro timer with server-client structure, written in C.
License:        GPL-3.0-or-later
URL:            https://github.com/nimaaskarian/potato-c
Source0:        potato-c-0.7.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A featureful, modular and fast pomodoro timer with server-client structure, written in C.

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.4-1
- Initial openEuler RISC-V package from the full package inventory.
