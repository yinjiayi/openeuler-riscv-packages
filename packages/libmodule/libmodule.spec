# SPDX-License-Identifier: Apache-2.0
Name:           libmodule
Version:        5.0.2
Release:        2%{?dist}
Summary:        C linux library to build simple and modular projects
License:        MIT
URL:            https://github.com/FedeDP/libmodule
Source0:        libmodule-5.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcmocka-devel
BuildRequires:  make

%description
C linux library to build simple and modular projects

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_TESTS=ON \
  -DBUILD_SAMPLES=OFF \
  -DBUILD_DOCS=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0.2-2
- Use the separate CMake build directory and declare the C++ compiler.
- Enable and run the upstream CMocka test suite.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
