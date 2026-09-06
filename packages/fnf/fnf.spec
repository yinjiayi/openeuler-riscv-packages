# SPDX-License-Identifier: Apache-2.0
Name:           fnf
Version:        0.4
Release:        1%{?dist}
Summary:        A simple fuzzy finder for the terminal
License:        MIT
URL:            https://github.com/leo-arch/fnf
Source0:        fnf-0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A simple fuzzy finder for the terminal

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Initial openEuler RISC-V package from the full package inventory.
