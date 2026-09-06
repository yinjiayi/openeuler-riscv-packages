# SPDX-License-Identifier: Apache-2.0
Name:           imagetransient
Version:        0.2.0
Release:        1%{?dist}
Summary:        Compact Qt 6 app for creating MP4 transition videos from two still images
License:        GPL-3.0-or-later
URL:            https://github.com/yousefvand/ImageTransient
Source0:        imagetransient-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Compact Qt 6 app for creating MP4 transition videos from two still images

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
