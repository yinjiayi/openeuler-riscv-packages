# SPDX-License-Identifier: Apache-2.0
Name:           range-v3
Version:        0.12.0
Release:        1%{?dist}
Summary:        Range library for C++11 and newer
License:        BSL-1.0
URL:            https://github.com/ericniebler/range-v3
Source0:        range-v3-0.12.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
range-v3 provides composable algorithms and range views for C++11 and newer.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DRANGE_V3_DOCS=OFF \
  -DRANGE_V3_EXAMPLES=OFF \
  -DRANGE_V3_TESTS=ON \
  -DRANGES_ENABLE_WERROR=OFF \
  -DRANGES_NATIVE=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/concepts/
%{_includedir}/meta/
%{_includedir}/range/
%{_libdir}/cmake/range-v3/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-1
- Initial openEuler RISC-V package.
