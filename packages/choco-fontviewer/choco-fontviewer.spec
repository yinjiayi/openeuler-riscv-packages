# SPDX-License-Identifier: Apache-2.0
Name:           choco-fontviewer
Version:        1.3.0
Release:        1%{?dist}
Summary:        View and install fonts with Google Fonts support
License:        GPL-2.0-or-later
URL:            https://github.com/chocolateimage/fontviewer
Source0:        choco-fontviewer-1.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
View and install fonts with Google Fonts support

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
