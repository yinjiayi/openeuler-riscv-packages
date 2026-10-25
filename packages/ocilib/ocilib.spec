# SPDX-License-Identifier: Apache-2.0
Name:           ocilib
Version:        4.8.0
Release:        1%{?dist}
Summary:        OCILIB (C and C++ Driver for Oracle)
License:        Apache-2.0
URL:            https://github.com/vrogier/ocilib
Source0:        ocilib-4.8.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
OCILIB (C and C++ Driver for Oracle)

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%license LICENSE
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
