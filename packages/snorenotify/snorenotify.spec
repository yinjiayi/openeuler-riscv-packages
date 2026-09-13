# SPDX-License-Identifier: Apache-2.0
Name:           snorenotify
Version:        0.7.0
Release:        6%{?dist}
Summary:        Multi-platform Qt5 notification framework
License:        LGPL-3.0-or-later
URL:            https://github.com/KDE/snorenotify
Source0:        snorenotify-0.7.0.tar.gz
Patch0:         0001-tests-link-display-test-to-qt-widgets.patch
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt5-qtbase-devel

%description
Multi-platform Qt5 notification framework

%prep
%autosetup -p1

%build
%cmake_conf -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
QT_QPA_PLATFORM=offscreen ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING.LGPL-3
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-6
- Link display_test to Qt Widgets so QTEST_MAIN creates QApplication.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-5
- Run the complete Qt test suite with the offscreen platform on headless CI.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-4
- Configure in the build directory consumed by the openEuler CMake macros.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-3
- Allow the complete required Qt5 dependency closure enough time to download.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-2
- Add the required ECM and Qt5 base development dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
