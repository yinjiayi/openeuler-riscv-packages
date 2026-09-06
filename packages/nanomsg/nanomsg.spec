# SPDX-License-Identifier: Apache-2.0
Name:           nanomsg
Version:        1.2.5
Release:        1%{?dist}
%global upstream_commit e6d0b8ddfc780eb89f8f6ef305e92c19e76bed6b
Summary:        Socket library implementing scalable messaging protocols
License:        MIT
URL:            https://nanomsg.org/
Source0:        1.2.5.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf

%description
nanomsg is a C socket library implementing scalable messaging protocols such
as pair, request/reply, publish/subscribe, pipeline, survey, and bus.

%package devel
Summary:        Development files for nanomsg
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, CMake and pkg-config metadata, and the unversioned linker name for
developing applications with nanomsg.

%prep
%autosetup -n nanomsg-%{upstream_commit} -p1

%build
%cmake_conf \
  -DNN_ENABLE_COVERAGE=OFF \
  -DNN_ENABLE_DOC=OFF \
  -DNN_ENABLE_NANOCAT=ON \
  -DNN_STATIC_LIB=OFF \
  -DNN_TESTS=ON \
  -DNN_TOOLS=ON
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license COPYING
%doc AUTHORS README.md RELEASING
%{_bindir}/nanocat
%{_libdir}/libnanomsg.so.6*

%files devel
%license COPYING
%{_includedir}/nanomsg/
%{_libdir}/libnanomsg.so
%{_libdir}/pkgconfig/nanomsg.pc
%{_libdir}/cmake/nanomsg-%{version}/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.4-1
- Initial openEuler RISC-V package with all 43 upstream CTests.
