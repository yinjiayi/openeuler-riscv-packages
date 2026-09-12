# SPDX-License-Identifier: Apache-2.0
Name:           nanomsg
Version:        1.2.5
Release:        2%{?dist}
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
%autosetup -n %{name}-%{version} -p1

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
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.5-2
- Use the versioned source archive root supplied by the 1.2.5 tag.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.4-1
- Initial openEuler RISC-V package with all 43 upstream CTests.
