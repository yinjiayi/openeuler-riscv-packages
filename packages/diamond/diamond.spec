# SPDX-License-Identifier: Apache-2.0
Name:           diamond
Version:        2.2.4
Release:        5%{?dist}
Summary:        High performance sequence aligner for protein and translated DNA searches with big sequence data. https://doi.org/10.1038/s41592-021-01101-x
License:        GPL-3.0-or-later
URL:            https://github.com/bbuchfink/diamond
Source0:        diamond-2.2.4.tar.gz
Patch0:         0001-cmake-detect-riscv-architecture.patch
Patch1:         0002-generic-build-fixes.patch
Patch2:         0003-global-ranking-use-serial-thread-pool-fallback.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

%description
High performance sequence aligner for protein and translated DNA searches with big sequence data. https://doi.org/10.1038/s41592-021-01101-x

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-5
- Keep global-ranking extension valid after the outer alignment pool is cleared.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-4
- Add the SQLite development headers required by the BLAST database reader.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-3
- Complete the portable fingerprint interface and remove a duplicate trait.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-2
- Detect RISC-V as non-x86 and probe the generic tuning compiler option

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-1
- Initial openEuler RISC-V package from the full package inventory.
