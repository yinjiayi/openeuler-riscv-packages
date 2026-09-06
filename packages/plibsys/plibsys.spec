# SPDX-License-Identifier: Apache-2.0
Name:           plibsys
Version:        0.0.5
Release:        1%{?dist}
Summary:        Cross-platform system C library with some helpful routines
License:        MIT
URL:            https://github.com/saprykin/plibsys
Source0:        plibsys-0.0.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Cross-platform system C library with some helpful routines

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
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
