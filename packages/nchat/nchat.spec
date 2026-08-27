# SPDX-License-Identifier: Apache-2.0
Name:           nchat
Version:        5.17.26
Release:        1%{?dist}
Summary:        Console-based chat client with support for Telegram
License:        MIT
URL:            https://github.com/d99kris/nchat
Source0:        nchat-5.17.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Console-based chat client with support for Telegram

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.17.26-1
- Initial openEuler RISC-V package from the full package inventory.
