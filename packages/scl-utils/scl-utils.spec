# SPDX-License-Identifier: Apache-2.0
Name:           scl-utils
Version:        2.0.3
Release:        3%{?dist}
Summary:        Utilities for alternative packaging
License:        GPL-2.0-or-later
URL:            https://github.com/sclorg/scl-utils
Source0:        scl-utils-2.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  rpm-devel

%description
Utilities for alternative packaging

%prep
%autosetup -p1

%build
%cmake_conf
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_mandir}/man1/scl.1' \
    -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
printf '/usr/share/man/man1/scl.1*\n' >> %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE


%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.3-3
- Keep the generated file list valid after RPM compresses the installed manual page.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.3-2
- Configure in the out-of-tree directory expected by the openEuler CMake macros.
- Declare the RPM and CMocka development dependencies used by the program and tests.
- Run the two upstream CTest executables and an installed-command smoke check.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
