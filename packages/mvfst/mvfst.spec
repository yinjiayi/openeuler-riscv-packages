# SPDX-License-Identifier: Apache-2.0
Name:           mvfst
Version:        2025.11.24.00
Release:        1%{?dist}
Summary:        An implementation of the QUIC transport protocol
License:        MIT
URL:            https://github.com/facebook/mvfst
Source0:        mvfst-2025.11.24.00.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An implementation of the QUIC transport protocol

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2025.11.24.00-1
- Initial openEuler RISC-V package from the full package inventory.
