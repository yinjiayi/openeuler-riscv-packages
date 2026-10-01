# SPDX-License-Identifier: Apache-2.0
Name:           libzlog
Version:        1.2.18
Release:        1%{?dist}
Summary:        a reliable pure C logging library
License:        Apache-2.0
URL:            https://github.com/hardysimpson/zlog
Source0:        libzlog-1.2.18.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
a reliable pure C logging library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.18-1
- Initial openEuler RISC-V package from the full package inventory.
