# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           cli11
Version:        2.7.2
Release:        1%{?dist}
Summary:        Header-only command-line parser for C++11 and newer
License:        BSD-3-Clause
URL:            https://github.com/CLIUtils/CLI11
Source0:        cli11-2.7.2.tar.gz
Source1:        catch-2.13.10.hpp
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
CLI11 is a header-only command-line parser for C++11 and newer.

%prep
%autosetup -p1 -n CLI11-%{version}

%build
mkdir -p riscv64-openEuler-linux-gnu/tests/catch2
install -pm 0644 %{SOURCE1} \
  riscv64-openEuler-linux-gnu/tests/catch2/catch.hpp
%cmake_conf \
  -DCLI11_BUILD_TESTS=ON \
  -DCLI11_BUILD_EXAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
# The Catch2-based test suite is complete but runs serially because concurrent
# target processes are unstable under QEMU user emulation.
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE
%doc README.md
%{_includedir}/CLI/
%{_datadir}/cmake/CLI11/
%{_datadir}/pkgconfig/CLI11.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.2-1
- Initial openEuler RISC-V package.
- Mark the header-only RPM noarch, disable empty debuginfo output, and serialize tests.
