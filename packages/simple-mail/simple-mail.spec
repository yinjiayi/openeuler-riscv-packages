# SPDX-License-Identifier: Apache-2.0
Name:           simple-mail
Version:        3.1.0
Release:        2%{?dist}
Summary:        SMTP Client Library for Qt
License:        LGPL-2.1-or-later
URL:            https://github.com/cutelyst/simple-mail
Source0:        simple-mail-3.1.0.tar.gz
Patch0:         0001-support-cmake-3.27.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(Qt5Core) >= 5.15.0
BuildRequires:  cmake(Qt5Network) >= 5.15.0
BuildRequires:  cmake(Qt5Widgets) >= 5.15.0

%description
SMTP Client Library for Qt

%package devel
Summary:        Development files for simple-mail
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, and pkg-config metadata for developing software
against simple-mail.

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
    -DQT_VERSION_MAJOR=5
%cmake_build

%install
%cmake_install

%check
# Upstream has no test targets; verify that the complete library and demo build
# produced every declared target before packaging.
test -e %{_vpath_builddir}/src/libSimpleMail3Qt5.so.%{version}
test -x %{_vpath_builddir}/demos/demo1/demo1
test -x %{_vpath_builddir}/demos/demo2/demo2
test -x %{_vpath_builddir}/demos/demo3/demo3
test -x %{_vpath_builddir}/demos/demo4/demo4
test -x %{_vpath_builddir}/demos/async1/async1

%files
%license LICENSE
%doc README.md
%{_libdir}/libSimpleMail3Qt5.so.0
%{_libdir}/libSimpleMail3Qt5.so.%{version}

%files devel
%{_includedir}/simplemail3-qt5/
%{_libdir}/cmake/SimpleMail3Qt5/
%{_libdir}/libSimpleMail3Qt5.so
%{_libdir}/pkgconfig/SimpleMail3Qt5.pc

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.0-2
- Support the target CMake 3.27 and configure an explicit out-of-tree Qt 5 build.
- Split runtime library and development files into their proper subpackages.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
