# SPDX-License-Identifier: Apache-2.0
Name:           nemo
Version:        6.6.4
Release:        1%{?dist}
Summary:        File manager for Cinnamon (Nautilus fork)
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/nemo
Source0:        nemo-6.6.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
File manager for Cinnamon (Nautilus fork)

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
%license COPYING.EXTENSIONS
%license COPYING.LIB
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
