# SPDX-License-Identifier: Apache-2.0
Name:           clib
Version:        2.8.7
Release:        1%{?dist}
Summary:        C package manager-ish
License:        MIT
URL:            https://github.com/clibs/clib
Source0:        clib-2.8.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
C package manager-ish

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.7-1
- Initial openEuler RISC-V package from the full package inventory.
