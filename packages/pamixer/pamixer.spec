# SPDX-License-Identifier: Apache-2.0
Name:           pamixer
Version:        1.6
Release:        1%{?dist}
Summary:        Pulseaudio command-line mixer like amixer
License:        GPL-3.0-or-later
URL:            https://github.com/cdemoulins/pamixer
Source0:        pamixer-1.6.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Pulseaudio command-line mixer like amixer

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
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
