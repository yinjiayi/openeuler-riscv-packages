# SPDX-License-Identifier: Apache-2.0
Name:           mount-zip
Version:        1.12
Release:        1%{?dist}
Summary:        FUSE file system for ZIP archives
License:        GPL-3.0-or-later
URL:            https://github.com/google/mount-zip
Source0:        mount-zip-1.12.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
FUSE file system for ZIP archives

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Initial openEuler RISC-V package from the full package inventory.
