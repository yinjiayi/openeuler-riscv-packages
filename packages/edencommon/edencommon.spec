# SPDX-License-Identifier: Apache-2.0
Name:           edencommon
Version:        2025.10.20.00
Release:        1%{?dist}
Summary:        Shared library for Watchman and Eden projects
License:        MIT
URL:            https://github.com/facebookexperimental/edencommon
Source0:        edencommon-2025.10.20.00.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Shared library for Watchman and Eden projects

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2025.10.20.00-1
- Initial openEuler RISC-V package from the full package inventory.
