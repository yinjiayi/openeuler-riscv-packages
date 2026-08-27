# SPDX-License-Identifier: Apache-2.0
Name:           wayfire-plugins-scale-ipc
Version:        1.1.0
Release:        1%{?dist}
Summary:        Extra IPC interaction for the scale plugin of Wayfire.
License:        Unlicense
URL:            https://github.com/dkondor/wayfire-scale-ipc
Source0:        wayfire-plugins-scale-ipc-1.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Extra IPC interaction for the scale plugin of Wayfire.

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
