# SPDX-License-Identifier: Apache-2.0
Name:           parlatype
Version:        4.3
Release:        1%{?dist}
Summary:        GNOME audio player for transcription
License:        GPL-3.0-or-later
URL:            https://github.com/gkarsay/parlatype
Source0:        parlatype-4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GNOME audio player for transcription

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3-1
- Initial openEuler RISC-V package from the full package inventory.
