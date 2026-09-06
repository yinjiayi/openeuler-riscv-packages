# SPDX-License-Identifier: Apache-2.0
Name:           qmarineplatformtheme5
Version:        0.3.0
Release:        1%{?dist}
Summary:        Another qt5ct for qt5, use toml as config
License:        MIT
URL:            https://github.com/Decodetalkers/qmarinetheme
Source0:        qmarineplatformtheme5-0.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Another qt5ct for qt5, use toml as config

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
