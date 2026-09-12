# SPDX-License-Identifier: Apache-2.0
Name:           libomemo
Version:        0.8.1
Release:        2%{?dist}
Summary:        Implementation of OMEMO (XEP-0384) in C
License:        MIT
URL:            https://github.com/gkdr/libomemo
Source0:        libomemo-0.8.1.tar.gz
Patch0:         patches/0001-port-to-mxml-4.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(mxml4)
BuildRequires:  pkgconfig(sqlite3)

%description
Implementation of OMEMO (XEP-0384) in C

%prep
%autosetup -p1

%build
%cmake_conf \
    -DOMEMO_INSTALL=ON \
    -DOMEMO_WITH_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure --no-tests=error

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-2
- Declare all pkg-config build providers and retain the complete three-test suite.
- Port the implementation and tests to the available parallel-installable Mini-XML 4 API.
- Configure in the out-of-tree directory expected by the openEuler CMake macros.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
