# SPDX-License-Identifier: Apache-2.0
Name:           wstroke
Version:        2.4.0
Release:        1%{?dist}
Summary:        a mouse gesture plug-in for wayfire. port of easystroke
License:        ISC
URL:            https://github.com/dkondor/wstroke
Source0:        wstroke-2.4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
a mouse gesture plug-in for wayfire. port of easystroke

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
