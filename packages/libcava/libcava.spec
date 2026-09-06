# SPDX-License-Identifier: Apache-2.0
Name:           libcava
Version:        1.0.0
Release:        1%{?dist}
Summary:        Fork to provide cava as a shared library, e.g. used by waybar. Cava is not provided as executable.
License:        MIT
URL:            https://github.com/LukashonakV/cava
Source0:        libcava-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Fork to provide cava as a shared library, e.g. used by waybar. Cava is not provided as executable.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
