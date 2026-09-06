# SPDX-License-Identifier: Apache-2.0
Name:           libcpufeatures
Version:        0.10.1
Release:        1%{?dist}
Summary:        A cross-platform C library to retrieve CPU features (such as available instructions) at runtime.
License:        Apache-2.0
URL:            https://github.com/google/cpu_features
Source0:        libcpufeatures-0.10.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A cross-platform C library to retrieve CPU features (such as available instructions) at runtime.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
