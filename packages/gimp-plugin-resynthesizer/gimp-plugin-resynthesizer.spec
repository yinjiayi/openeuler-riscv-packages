# SPDX-License-Identifier: Apache-2.0
Name:           gimp-plugin-resynthesizer
Version:        3.0.1
Release:        1%{?dist}
Summary:        Suite of gimp plugins for texture synthesis
License:        GPL-3.0-or-later
URL:            https://github.com/bootchk/resynthesizer
Source0:        gimp-plugin-resynthesizer-3.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Suite of gimp plugins for texture synthesis

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
