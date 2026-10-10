# SPDX-License-Identifier: Apache-2.0
Name:           gpu-screen-recorder-qt
Version:        5.7.9
Release:        1%{?dist}
Summary:        Qt6 UI for gpu-screen-recorder
License:        GPL-3.0-or-later
URL:            https://github.com/Coobyk/gpu-screen-recorder-qt
Source0:        gpu-screen-recorder-qt-5.7.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt6 UI for gpu-screen-recorder

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.7.9-1
- Initial openEuler RISC-V package from the full package inventory.
