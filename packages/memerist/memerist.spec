# SPDX-License-Identifier: Apache-2.0
Name:           memerist
Version:        1.0.0
Release:        1%{?dist}
Summary:        A modern meme editor built with GTK 4 and Libadwaita
License:        GPL-3.0-or-later
URL:            https://github.com/vani-tty1/memerist
Source0:        memerist-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A modern meme editor built with GTK 4 and Libadwaita

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
