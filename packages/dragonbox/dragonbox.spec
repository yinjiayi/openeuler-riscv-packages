# SPDX-License-Identifier: Apache-2.0
Name:           dragonbox
Version:        1.1.3
Release:        1%{?dist}
Summary:        Header-only float-to-string conversion library
License:        Apache-2.0 WITH LLVM-exception OR BSL-1.0
URL:            https://github.com/jk-jeon/dragonbox
Source0:        dragonbox-1.1.3.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Dragonbox converts IEEE-754 floating-point values to decimal representations.
It provides a header-only core and an optional static to-chars implementation.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%{__cxx} %{optflags} -std=c++17 -Iinclude source/dragonbox_to_chars.cpp \
  -x c++ -o dragonbox-smoke - <<'EOF'
#include "dragonbox/dragonbox_to_chars.h"
#include <cstdio>
int main() {
  char buffer[64];
  char *end = jkj::dragonbox::to_chars(1.25, buffer);
  *end = '\0';
  std::puts(buffer);
  return 0;
}
EOF
./dragonbox-smoke | grep -F '1.25'

%files
%license LICENSE-Apache2-LLVM LICENSE-Boost
%doc README.md
%{_includedir}/dragonbox-%{version}/
%{_libdir}/libdragonbox_to_chars.a
%{_libdir}/cmake/dragonbox-%{version}/

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-1
- Initial openEuler RISC-V package.

