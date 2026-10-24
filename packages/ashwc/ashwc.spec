# SPDX-License-Identifier: Apache-2.0
Name:           ashwc
Version:        0.2.0
Release:        1%{?dist}
Summary:        a minimal wayland compositor with various layouts, animations and all the eye-candy
License:        MIT
URL:            https://github.com/shadowash8/ashwc
Source0:        ashwc-0.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
a minimal wayland compositor with various layouts, animations and all the eye-candy

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
