# SPDX-License-Identifier: Apache-2.0
Name:           pipelam
Version:        0.1.14
Release:        1%{?dist}
Summary:        A lightweight GTK4-based notification system for displaying text, images, and progress bars
License:        MIT
URL:            https://github.com/thomascrha/pipelam
Source0:        pipelam-0.1.14.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A lightweight GTK4-based notification system for displaying text, images, and progress bars

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.14-1
- Initial openEuler RISC-V package from the full package inventory.
