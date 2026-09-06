# SPDX-License-Identifier: Apache-2.0
Name:           libunarr
Version:        1.1.1
Release:        1%{?dist}
Summary:        A lightweight decompression library with support for rar, tar and zip archives.
License:        LGPL-3.0-or-later
URL:            https://github.com/selmf/unarr
Source0:        libunarr-1.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A lightweight decompression library with support for rar, tar and zip archives.

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
