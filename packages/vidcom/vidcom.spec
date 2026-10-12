# SPDX-License-Identifier: Apache-2.0
Name:           vidcom
Version:        0.82
Release:        1%{?dist}
Summary:        Archive your videos
License:        GPL-3.0-or-later
URL:            https://github.com/seja-arctic-fox/vidcom
Source0:        vidcom-0.82.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Archive your videos

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.82-1
- Initial openEuler RISC-V package from the full package inventory.
