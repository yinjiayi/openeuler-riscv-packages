# SPDX-License-Identifier: Apache-2.0
Name:           kiwix-tools
Version:        3.8.2
Release:        1%{?dist}
Summary:        kiwix command line tools
License:        GPL-3.0-or-later
URL:            https://github.com/kiwix/kiwix-tools
Source0:        kiwix-tools-3.8.2.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
kiwix command line tools

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
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
