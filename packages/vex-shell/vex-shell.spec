# SPDX-License-Identifier: Apache-2.0
Name:           vex-shell
Version:        0.1.1
Release:        1%{?dist}
Summary:        A typed shell with structured data pipelines, written in C
License:        MIT
URL:            https://github.com/aethstetic/vex
Source0:        vex-shell-0.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A typed shell with structured data pipelines, written in C

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
