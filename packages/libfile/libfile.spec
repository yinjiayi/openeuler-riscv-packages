# SPDX-License-Identifier: Apache-2.0
Name:           libfile
Version:        1.0.2
Release:        1%{?dist}
Summary:        File library for checking types and architecture.
License:        MIT
URL:            https://github.com/coolguy-09/libfile
Source0:        libfile-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
File library for checking types and architecture.

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
