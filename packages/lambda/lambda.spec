# SPDX-License-Identifier: Apache-2.0
Name:           lambda
Version:        0.2
Release:        1%{?dist}
Summary:        Lambda calculus beta reduction playground with optional eta and ncurses/CLI front ends
License:        GPL-3.0-or-later
URL:            https://github.com/drmenguin/lambda
Source0:        lambda-0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Lambda calculus beta reduction playground with optional eta and ncurses/CLI front ends

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Initial openEuler RISC-V package from the full package inventory.
