# SPDX-License-Identifier: Apache-2.0
Name:           wf-recorder
Version:        0.6.0
Release:        1%{?dist}
Summary:        Screen recorder for wlroots-based compositors such as sway
License:        MIT
URL:            https://github.com/ammen99/wf-recorder
Source0:        wf-recorder-0.6.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Screen recorder for wlroots-based compositors such as sway

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
