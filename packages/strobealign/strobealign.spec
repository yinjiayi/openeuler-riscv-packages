# SPDX-License-Identifier: Apache-2.0
Name:           strobealign
Version:        0.16.0
Release:        1%{?dist}
Summary:        Aligns short reads using dynamic seed size with strobemers. https://doi.org/10.1186/s13059-022-02831-7
License:        MIT
URL:            https://github.com/ksahlin/strobealign
Source0:        strobealign-0.16.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Aligns short reads using dynamic seed size with strobemers. https://doi.org/10.1186/s13059-022-02831-7

%prep
%autosetup -p1

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16.0-1
- Initial openEuler RISC-V package from the full package inventory.
