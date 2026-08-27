# SPDX-License-Identifier: Apache-2.0
Name:           timepad
Version:        0.1.0
Release:        1%{?dist}
Summary:        A minimal Timer App for Linux that has a picture-in-picture mode
License:        MIT
URL:            https://github.com/agokule/timepad
Source0:        timepad-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A minimal Timer App for Linux that has a picture-in-picture mode

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
