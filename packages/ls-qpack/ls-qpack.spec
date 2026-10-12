# SPDX-License-Identifier: Apache-2.0
Name:           ls-qpack
Version:        2.6.2
Release:        1%{?dist}
Summary:        QPACK compression library for use with HTTP/3
License:        MIT
URL:            https://github.com/litespeedtech/ls-qpack
Source0:        ls-qpack-2.6.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
QPACK compression library for use with HTTP/3

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.2-1
- Initial openEuler RISC-V package from the full package inventory.
