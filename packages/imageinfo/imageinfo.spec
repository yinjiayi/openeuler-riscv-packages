# SPDX-License-Identifier: Apache-2.0
Name:           imageinfo
Version:        2.0.0
Release:        1%{?dist}
Summary:        Cross platform super fast single header c++ library to get image size and format without loading/decoding
License:        MIT
URL:            https://github.com/xiaozhuai/imageinfo
Source0:        imageinfo-2.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Cross platform super fast single header c++ library to get image size and format without loading/decoding

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
