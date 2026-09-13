# SPDX-License-Identifier: Apache-2.0
Name:           vvenc
Version:        1.14.0
Release:        1%{?dist}
Summary:        A H.266/VVC (Versatile Video Coding) encoder
License:        BSD-3-Clause-Clear
URL:            https://github.com/fraunhoferhhi/vvenc
Source0:        vvenc-1.14.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A H.266/VVC (Versatile Video Coding) encoder

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14.0-1
- Initial openEuler RISC-V package from the full package inventory.
