# SPDX-License-Identifier: Apache-2.0
Name:           uftrace
Version:        0.19
Release:        1%{?dist}
Summary:        Function graph tracer for C/C++/Rust
License:        GPL-2.0-or-later
URL:            https://github.com/namhyung/uftrace
Source0:        uftrace-0.19.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Function graph tracer for C/C++/Rust

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
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19-1
- Initial openEuler RISC-V package from the full package inventory.
