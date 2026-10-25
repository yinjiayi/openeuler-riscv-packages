# SPDX-License-Identifier: Apache-2.0
Name:           albafetch
Version:        4.3
Release:        1%{?dist}
Summary:        Neofetch, but written in C; both faster and worse than the original
License:        MIT
URL:            https://github.com/alba4k/albafetch
Source0:        albafetch-4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Neofetch, but written in C; both faster and worse than the original

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3-1
- Initial openEuler RISC-V package from the full package inventory.
