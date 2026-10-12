# SPDX-License-Identifier: Apache-2.0
Name:           google-crc32c
Version:        1.1.2
Release:        1%{?dist}
Summary:        CRC32C implementation with hardware acceleration
License:        BSD-3-Clause
URL:            https://github.com/google/crc32c
Source0:        google-crc32c-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
google-crc32c computes CRC32C checksums and dispatches to suitable hardware
accelerated or portable implementations.

%package devel
Summary:        Development files for google-crc32c
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, and the unversioned library link for developing with
google-crc32c.

%prep
%autosetup -p1 -n crc32c-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DCRC32C_BUILD_BENCHMARKS=OFF \
  -DCRC32C_BUILD_TESTS=OFF \
  -DCRC32C_INSTALL=ON \
  -DCRC32C_USE_GLOG=OFF
%cmake_build

%install
%cmake_install

%check
cat > crc32c-smoke.cc <<'EOF'
#include <cstdint>
#include <crc32c/crc32c.h>

int main() {
    const std::uint8_t input[] = "123456789";
    return crc32c_value(input, sizeof(input) - 1) == UINT32_C(0xe3069283) ? 0 : 1;
}
EOF
%{__cxx} %{optflags} -std=c++11 crc32c-smoke.cc \
  -I%{buildroot}%{_includedir} -L%{buildroot}%{_libdir} \
  -Wl,-rpath,%{buildroot}%{_libdir} -lcrc32c -o crc32c-smoke
./crc32c-smoke

%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libcrc32c.so.1*

%files devel
%license LICENSE
%{_includedir}/crc32c/
%{_libdir}/libcrc32c.so
%{_libdir}/cmake/Crc32c/

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial package from the official 1.1.2 tag archive.
- Keep a deterministic installed C API check while the tag archive's empty
  submodule directories leave optional upstream test dependencies unavailable.
