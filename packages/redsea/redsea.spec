# SPDX-License-Identifier: Apache-2.0
Name:           redsea
Version:        1.3.1
Release:        1%{?dist}
Summary:        RDS decoder for the command line
License:        MIT
URL:            https://github.com/windytan/redsea
Source0:        redsea-1.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
RDS decoder for the command line

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
