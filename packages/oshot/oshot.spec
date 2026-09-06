# SPDX-License-Identifier: Apache-2.0
Name:           oshot
Version:        0.4.6
Release:        1%{?dist}
Summary:        A fast and lightweight screenshot tool for extracting text on the fly
License:        BSD-3-Clause
URL:            https://github.com/Toni500github/oshot
Source0:        oshot-0.4.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast and lightweight screenshot tool for extracting text on the fly

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.6-1
- Initial openEuler RISC-V package from the full package inventory.
