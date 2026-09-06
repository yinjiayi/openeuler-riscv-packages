# SPDX-License-Identifier: Apache-2.0
Name:           intel-lms
Version:        2625.0.0.0
Release:        2%{?dist}
Summary:        Allows applications to access the Intel AMT firmware via the Intel MEI
License:        Apache-2.0
URL:            https://github.com/intel/lms
Source0:        intel-lms-2625.0.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Allows applications to access the Intel AMT firmware via the Intel MEI

%prep
%autosetup -n lms-%{version} -p1

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

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2625.0.0.0-2
- Enter the verified GitHub tag archive's lms-version root during prep.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2625.0.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
