# SPDX-License-Identifier: Apache-2.0
Name:           dragon-tea
Version:        1.0.7
Release:        1%{?dist}
Summary:        Dragon Tea. Free Messenger
License:        GPL-3.0-or-later
URL:            https://github.com/badcast/dragon-tea
Source0:        dragon-tea-1.0.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Dragon Tea. Free Messenger

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Initial openEuler RISC-V package from the full package inventory.
