# SPDX-License-Identifier: Apache-2.0
Name:           pato
Version:        1.0.1
Release:        3%{?dist}
Summary:        PATO: high PerformAnce TriplexatOr is a high performance tool for the fast and efficient detection of triple helices and triplex features in nucleotide sequ
License:        MIT
URL:            https://github.com/UDC-GAC/PATO
Source0:        pato-1.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
PATO: high PerformAnce TriplexatOr is a high performance tool for the fast and efficient detection of triple helices and triplex features in nucleotide sequ

%prep
%autosetup -n PATO-%{version} -p1

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
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-3
- Configure the explicit CMake source and out-of-source build directories.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-2
- Match the exact top-level directory in the official source archive.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
