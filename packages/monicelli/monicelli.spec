# SPDX-License-Identifier: Apache-2.0
Name:           monicelli
Version:        2.3.0
Release:        1%{?dist}
Summary:        An esoterical programming language based on the so-called "supercazzole" from the movie Amici Miei, a masterpiece of the Italian comedy.
License:        GPL-3.0-or-later
URL:            https://github.com/esseks/monicelli
Source0:        monicelli-2.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An esoterical programming language based on the so-called "supercazzole" from the movie Amici Miei, a masterpiece of the Italian comedy.

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
