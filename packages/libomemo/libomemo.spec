# SPDX-License-Identifier: Apache-2.0
Name:           libomemo
Version:        0.8.1
Release:        4%{?dist}
Summary:        Implementation of OMEMO (XEP-0384) in C
# The independent C library is MIT; upstream CMakeLists.txt is GPL-2.0-or-later.
License:        MIT AND GPL-2.0-or-later
URL:            https://github.com/gkdr/libomemo
Source0:        libomemo-0.8.1.tar.gz
Source1:        GPL-2.0.txt
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
cp -p %{SOURCE1} GPL-2.0.txt

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
%license LICENSE GPL-2.0.txt
%doc README.md

%changelog
* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-4
- Materialize the pinned GPL document in the source tree before relative license packaging.
- Fix RPM's special-license path-mode conflict without changing source or default tests.

* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-3
- Preserve the upstream build script's GPL-2.0-or-later notice and ship pinned full GPL2 terms.
- Document the separate MIT library and GPL build-file license scopes without relicensing either.
- Keep the upstream source, Mini-XML compatibility patch and all three original tests unchanged.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-2
- Declare all pkg-config build providers and retain the complete three-test suite.
- Port the implementation and tests to the available parallel-installable Mini-XML 4 API.
- Configure in the out-of-tree directory expected by the openEuler CMake macros.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
