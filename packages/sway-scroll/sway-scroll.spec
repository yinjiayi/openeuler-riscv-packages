# SPDX-License-Identifier: Apache-2.0
Name:           sway-scroll
Version:        1.12.17
Release:        1%{?dist}
Summary:        Fork of the sway Wayland compositor with a scrolling layout like PaperWM or niri (stable version)
License:        MIT
URL:            https://github.com/dawsers/scroll
Source0:        sway-scroll-1.12.17.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Fork of the sway Wayland compositor with a scrolling layout like PaperWM or niri (stable version)

%prep
%autosetup -n scroll-%{version} -p1

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.17-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
