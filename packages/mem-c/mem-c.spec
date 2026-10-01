# SPDX-License-Identifier: Apache-2.0
Name:           mem-c
Version:        1.1.4
Release:        1%{?dist}
Summary:        mem-c is a simple memory allocator using a heap data structure with the mmap Linux syscall for dynamic memory management. It has a worst-case search time of
License:        MIT
URL:            https://github.com/alecksandr26/mem-c
Source0:        mem-c-1.1.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
mem-c is a simple memory allocator using a heap data structure with the mmap Linux syscall for dynamic memory management. It has a worst-case search time of

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
