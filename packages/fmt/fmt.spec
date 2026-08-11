# SPDX-License-Identifier: Apache-2.0
Name:           fmt
Version:        12.2.0
Release:        1%{?dist}
Summary:        Modern formatting library for C++
License:        MIT
URL:            https://fmt.dev
Source0:        fmt-12.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
fmt is a safe, fast formatting library for modern C++.

%package devel
Summary:        Development files for fmt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and build-system metadata for developing applications with fmt.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DFMT_DOC=OFF \
  -DFMT_TEST=ON
%cmake_build

%install
%cmake_install

%check
# The ctest RPM macro still leaves the build macro's own -j2 in effect. Invoke
# CTest directly so target processes are genuinely serialized under QEMU.
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE
%doc README.md
%{_libdir}/libfmt.so.12*

%files devel
%license LICENSE
%{_includedir}/fmt/
%{_libdir}/libfmt-c.a
%{_libdir}/libfmt.so
%{_libdir}/cmake/fmt/
%{_libdir}/pkgconfig/fmt.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 12.2.0-1
- Initial openEuler RISC-V package.
- Package the upstream fmt-c static archive and truly serialize QEMU tests.
