# SPDX-License-Identifier: Apache-2.0
Name:           indicators
Version:        2.3
Release:        1%{?dist}
Summary:        Activity Indicators for Modern C++
License:        MIT
URL:            https://github.com/p-ranav/indicators
Source0:        indicators-2.3.tar.gz
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Activity Indicators for Modern C++

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) \
  ! -path '%{buildroot}%{_licensedir}/%{name}/*' \
  -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%license LICENSE.termcolor
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3-1
- Initial openEuler RISC-V package from the full package inventory.
