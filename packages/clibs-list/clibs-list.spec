# SPDX-License-Identifier: Apache-2.0
Name:           clibs-list
Version:        0.4.1
Release:        1%{?dist}
Summary:        C doubly linked list implementation
License:        MIT
URL:            https://github.com/clibs/list
Source0:        clibs-list-0.4.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
C doubly linked list implementation

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
