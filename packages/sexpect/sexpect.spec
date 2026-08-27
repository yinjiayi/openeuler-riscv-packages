# SPDX-License-Identifier: Apache-2.0
Name:           sexpect
Version:        2.3.15
Release:        1%{?dist}
Summary:        Expect for shells
License:        GPL-3.0-or-later
URL:            https://github.com/clarkwang/sexpect
Source0:        sexpect-2.3.15.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Expect for shells

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.15-1
- Initial openEuler RISC-V package from the full package inventory.
