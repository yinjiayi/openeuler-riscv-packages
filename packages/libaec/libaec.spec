# SPDX-License-Identifier: Apache-2.0
Name:           libaec
Version:        1.1.7
Release:        1%{?dist}
Summary:        Adaptive Entropy Coding library
License:        BSD-2-Clause
URL:            https://github.com/Deutsches-Klimarechenzentrum/libaec
Source0:        libaec-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
libaec implements lossless Adaptive Entropy Coding for low-entropy integer
data and supplies an SZIP-compatible shared library.

%package devel
Summary:        Development files for libaec
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake package metadata, and unversioned linker names for libaec and
its SZIP compatibility library.

%package help
Summary:        Documentation for libaec
BuildArch:      noarch

%description help
Upstream design, compatibility, installation, patent, and release notes for
libaec.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%ctest --parallel 1

%files
%license LICENSE.txt
%{_libdir}/libaec.so.0*
%{_libdir}/libsz.so.2*

%files devel
%license LICENSE.txt
%{_includedir}/libaec.h
%{_includedir}/szlib.h
%{_libdir}/libaec.so
%{_libdir}/libsz.so
%{_libdir}/cmake/libaec/

%files help
%license LICENSE.txt
%doc CHANGELOG.md INSTALL.md README.md README.SZIP doc/patent.txt

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.7-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
