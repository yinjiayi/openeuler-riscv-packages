# SPDX-License-Identifier: Apache-2.0
Name:           quill
Version:        12.1.0
Release:        1%{?dist}
Summary:        Asynchronous Low Latency C++ Logging Library
License:        MIT
URL:            https://github.com/odygrd/quill
Source0:        quill-12.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Asynchronous Low Latency C++ Logging Library

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 12.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
