# SPDX-License-Identifier: Apache-2.0
Name:           nvidia-system-monitor-qt
Version:        1.6
Release:        1%{?dist}
Summary:        Task Manager for Linux for Nvidia graphics cards (QT vesrion)
License:        MIT
URL:            https://github.com/congard/nvidia-system-monitor-qt
Source0:        nvidia-system-monitor-qt-1.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Task Manager for Linux for Nvidia graphics cards (QT vesrion)

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
