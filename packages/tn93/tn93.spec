# SPDX-License-Identifier: Apache-2.0
Name:           tn93
Version:        1.0.16
Release:        1%{?dist}
Summary:        TN93 fast distance calculator
License:        MIT
URL:            https://github.com/veg/tn93
Source0:        tn93-1.0.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
TN93 fast distance calculator

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.16-1
- Initial openEuler RISC-V package from the full package inventory.
