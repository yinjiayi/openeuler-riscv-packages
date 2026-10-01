# SPDX-License-Identifier: Apache-2.0
Name:           pacutils
Version:        0.15.0
Release:        1%{?dist}
Summary:        Helper tools for libalpm
License:        MIT
URL:            https://github.com/andrewgregory/pacutils
Source0:        pacutils-0.15.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Helper tools for libalpm

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
%license COPYING


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15.0-1
- Initial openEuler RISC-V package from the full package inventory.
