# SPDX-License-Identifier: Apache-2.0
Name:           pacenv
Version:        0.1.1
Release:        1%{?dist}
Summary:        Creation and management of lightweight GNU/Linux environments
License:        MIT
URL:            https://github.com/beryll1um/pacenv
Source0:        pacenv-0.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Creation and management of lightweight GNU/Linux environments

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
