# SPDX-License-Identifier: Apache-2.0
Name:           procmon
Version:        2.2.1
Release:        2%{?dist}
Summary:        Trace syscall activity tool
License:        MIT
URL:            https://github.com/microsoft/ProcMon-for-Linux
Source0:        procmon-2.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Trace syscall activity tool

%prep
%autosetup -n ProcMon-for-Linux-%{version} -p1

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
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-2
- Match the official tag archive's top-level source directory.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
