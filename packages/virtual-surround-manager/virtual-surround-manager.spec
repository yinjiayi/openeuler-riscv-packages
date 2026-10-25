# SPDX-License-Identifier: Apache-2.0
Name:           virtual-surround-manager
Version:        1.3.1
Release:        1%{?dist}
Summary:        3D sound for headphones
License:        MIT
URL:            https://github.com/Berny23/virtual-surround-manager
Source0:        virtual-surround-manager-1.3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
3D sound for headphones

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
