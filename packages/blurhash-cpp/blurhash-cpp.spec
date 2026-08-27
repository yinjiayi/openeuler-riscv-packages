# SPDX-License-Identifier: Apache-2.0
Name:           blurhash-cpp
Version:        0.2.0
Release:        1%{?dist}
Summary:        C++ blurhash encoder/decoder
License:        BSL-1.0
URL:            https://github.com/Nheko-Reborn/blurhash
Source0:        blurhash-cpp-0.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
C++ blurhash encoder/decoder

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
