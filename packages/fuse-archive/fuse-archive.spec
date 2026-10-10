# SPDX-License-Identifier: Apache-2.0
Name:           fuse-archive
Version:        1.16
Release:        1%{?dist}
Summary:        FUSE file system for archives and compressed files (ZIP, RAR, 7Z, ISO, TGZ, XZ...)
License:        Apache-2.0
URL:            https://github.com/google/fuse-archive
Source0:        fuse-archive-1.16.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
FUSE file system for archives and compressed files (ZIP, RAR, 7Z, ISO, TGZ, XZ...)

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Initial openEuler RISC-V package from the full package inventory.
