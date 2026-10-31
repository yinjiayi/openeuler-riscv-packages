# SPDX-License-Identifier: Apache-2.0
Name:           stegseek
Version:        0.6
Release:        1%{?dist}
Summary:        Lightning fast steghide cracker
License:        GPL-2.0-or-later
URL:            https://github.com/RickdeJager/stegseek
Source0:        stegseek-0.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Lightning fast steghide cracker

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6-1
- Initial openEuler RISC-V package from the full package inventory.
