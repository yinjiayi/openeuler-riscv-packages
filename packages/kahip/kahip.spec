# SPDX-License-Identifier: Apache-2.0
Name:           kahip
Version:        3.25
Release:        3%{?dist}
Summary:        Karlsruhe HIGH Quality Partitioning
License:        MIT
URL:            https://github.com/KaHIP/KaHIP
Source0:        kahip-3.25.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  openmpi-devel

%description
Karlsruhe HIGH Quality Partitioning

%prep
%autosetup -n KaHIP-%{version} -p1

%build
%cmake_conf -DNONATIVEOPTIMIZATIONS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/interface_test > interface-test.log
grep -F 'partitioning graph from the manual' interface-test.log
grep -E '^edge cut [0-9]+$' interface-test.log
grep -E '^qap [0-9]+$' interface-test.log

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.25-3
- Extend the QEMU budget after the full MPI build reached 72% at the deadline.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.25-2
- Fix the source directory, retain MPI and ParHIP support, and exercise the interface.
- Disable host-native compiler tuning for the RVA23 package target.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.25-1
- Initial openEuler RISC-V package from the full package inventory.
