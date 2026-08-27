# SPDX-License-Identifier: Apache-2.0
Name:           dreamchess
Version:        0.3.0
Release:        1%{?dist}
Summary:        An open source chess game. It comes with its own engine called Dreamer
License:        GPL-3.0-or-later
URL:            https://github.com/dreamchess/dreamchess
Source0:        dreamchess-0.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
An open source chess game. It comes with its own engine called Dreamer

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
%license LICENSE.txt
%doc README.md
%doc NEWS.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
