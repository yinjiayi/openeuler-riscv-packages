# SPDX-License-Identifier: Apache-2.0
Name:           libxdgdirs
Version:        1.1.3
Release:        3%{?dist}
Summary:        An implementation helpers for XDG Base Directory Specification in C
License:        MIT
URL:            https://github.com/Jorenar/libXDGdirs
Source0:        libxdgdirs-1.1.3.tar.gz
Patch0:         0001-cmake-run-tests-with-build-testing.patch
Patch1:         0002-tests-export-xdg-data-home.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
An implementation helpers for XDG Base Directory Specification in C

%prep
%autosetup -p1 -n libXDGdirs-%{version}

%build
%cmake_conf -DBUILD_TESTING=ON
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
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-3
- Export the test XDG_DATA_HOME value to the child process under test.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-2
- Select the verified archive root and run tests in an out-of-source release build.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
