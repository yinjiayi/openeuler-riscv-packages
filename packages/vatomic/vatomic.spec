# SPDX-License-Identifier: Apache-2.0
Name:           vatomic
Version:        2.4.1
Release:        1%{?dist}
Summary:        VSync atomics - formally-verified atomic operations library
License:        MIT
URL:            https://github.com/open-s4c/vatomic
Source0:        vatomic-2.4.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
VSync atomics - formally-verified atomic operations library

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
