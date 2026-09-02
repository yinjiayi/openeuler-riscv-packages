# SPDX-License-Identifier: Apache-2.0
Name:           task-automation
Version:        0.1.0
Release:        2%{?dist}
Summary:        KDE Plasma Wayland task recorder and player for keyboard, mouse, wheel, and timing automation
License:        MIT
URL:            https://github.com/yousefvand/Task-Automation
Source0:        task-automation-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel

%description
KDE Plasma Wayland task recorder and player for keyboard, mouse, wheel, and timing automation

%prep
%autosetup -n Task-Automation-%{version} -p1

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
* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-2
- Match the official archive root and add the required Qt 6 development files.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
