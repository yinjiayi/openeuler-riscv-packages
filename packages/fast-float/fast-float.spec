# SPDX-License-Identifier: Apache-2.0
Name:           fast-float
Version:        8.2.10
Release:        1%{?dist}
Summary:        Fast and exact string-to-floating-point conversion library
License:        Apache-2.0 OR BSL-1.0 OR MIT
URL:            https://github.com/fastfloat/fast_float
Source0:        fast-float-%{version}.tar.gz
Source1:        doctest-2.5.2.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

BuildArch:      noarch

%description
fast_float is a header-only C++ library for locale-independent, exact parsing
of decimal strings into binary floating-point values.

%prep
%autosetup -p1 -n fast_float-%{version} -a 1

%build
%cmake_conf \
  -DFASTFLOAT_CXX_STANDARD=17 \
  -DFASTFLOAT_INSTALL=ON \
  -DFASTFLOAT_TEST=ON \
  -DFASTFLOAT_SUPPLEMENTAL_TESTS=OFF \
  -DSYSTEM_DOCTEST=OFF \
  -DFETCHCONTENT_SOURCE_DIR_DOCTEST=%{_builddir}/fast_float-%{version}/doctest-2.5.2
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE-APACHE LICENSE-BOOST LICENSE-MIT
%doc AUTHORS CONTRIBUTORS README.md
%{_includedir}/fast_float/
%{_datadir}/cmake/FastFloat/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.2.10-1
- Run the upstream test suite offline with a pinned doctest release.
- Exclude only supplemental data fetched from an unpinned mutable branch.
- Initial openEuler RISC-V package.
