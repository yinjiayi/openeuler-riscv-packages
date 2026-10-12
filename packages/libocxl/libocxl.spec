# SPDX-License-Identifier: Apache-2.0
Name:           libocxl
Version:        1.2.1
Release:        1%{?dist}
Summary:        Allows to implement a user-space driver for an OpenCAPI accelerator
License:        Apache-2.0
URL:            https://github.com/OpenCAPI/libocxl
Source0:        libocxl-1.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Allows to implement a user-space driver for an OpenCAPI accelerator

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
