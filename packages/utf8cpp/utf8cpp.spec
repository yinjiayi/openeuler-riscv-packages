# SPDX-License-Identifier: Apache-2.0
Name:           utf8cpp
Version:        4.2.0
Release:        1%{?dist}
Summary:        Portable header-only library for UTF-8 encoded strings
License:        BSL-1.0
URL:            https://github.com/nemtrif/utfcpp
Source0:        v4.2.0.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

BuildArch:      noarch

%description
utf8cpp is a portable, lightweight, header-only C++ library for iterating,
validating, and converting UTF-8 encoded strings.

%prep
%autosetup -p1 -n utfcpp-%{version}

%build
%cmake_conf \
  -DUTF8CPP_ENABLE_BENCHMARKS=OFF \
  -DUTF8CPP_ENABLE_TESTS=ON
%cmake_build

%install
%cmake_install

# The generated CMake package metadata must follow the RPM version.
config_version=%{buildroot}%{_datadir}/utf8cpp/cmake/utf8cppConfigVersion.cmake
grep -Fq 'set(PACKAGE_VERSION "%{version}")' "$config_version"

%check
%ctest

%files
%license LICENSE
%doc API_REFERENCE.md README.md
%{_includedir}/utf8cpp/
%{_datadir}/utf8cpp/

%changelog
* Mon Aug 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.0-1
- Update to 4.2.0 and accept its corrected generated CMake package version.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.1-1
- Initial openEuler RISC-V package with all six upstream CTest programs.
- Correct the generated CMake package version after verifying upstream's known 4.1.0 value.
