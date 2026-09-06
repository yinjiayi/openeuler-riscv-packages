# SPDX-License-Identifier: Apache-2.0
Name:           minisign
Version:        0.12
Release:        1%{?dist}
Summary:        A dead-simple tool to sign files and verify digital signatures
License:        ISC
URL:            https://github.com/jedisct1/minisign
Source0:        minisign-0.12.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A dead-simple tool to sign files and verify digital signatures

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Initial openEuler RISC-V package from the full package inventory.
