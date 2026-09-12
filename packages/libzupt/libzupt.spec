# SPDX-License-Identifier: Apache-2.0
Name:           libzupt
Version:        1.0.8
Release:        2%{?dist}
Summary:        Post-quantum hybrid cryptography library
License:        MIT
URL:            https://github.com/cabelo/libzupt
Source0:        libzupt-1.0.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Post-quantum hybrid cryptography library

%prep
%autosetup -p1

%build
%cmake_conf \
  -DLIBZUPT_BUILD_TESTS=ON \
  -DLIBZUPT_BUILD_EXAMPLES=OFF \
  -DLIBZUPT_BUILD_PYTHON=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure --no-tests=error

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-2
- Use the openEuler out-of-source CMake workflow and run the upstream test suite.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
