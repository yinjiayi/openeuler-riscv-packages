# SPDX-License-Identifier: Apache-2.0
Name:           geany-plugin-preview
Version:        0.2.4
Release:        1%{?dist}
Summary:        Plugin for Geany to preview markdown and other markup languages
License:        GPL-3.0-or-later
URL:            https://github.com/xiota/geany-preview
Source0:        geany-plugin-preview-0.2.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Plugin for Geany to preview markdown and other markup languages

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.4-1
- Initial openEuler RISC-V package from the full package inventory.
