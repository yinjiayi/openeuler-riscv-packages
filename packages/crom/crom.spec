# SPDX-License-Identifier: Apache-2.0
Name:           crom
Version:        0.3.1
Release:        1%{?dist}
Summary:        Fast parallel file finder by name or content, freestanding, no libc
License:        MIT
URL:            https://github.com/hedgeg0d/crom
Source0:        crom-0.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Fast parallel file finder by name or content, freestanding, no libc

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
