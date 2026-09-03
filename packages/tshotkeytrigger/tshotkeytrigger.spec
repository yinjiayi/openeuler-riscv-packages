# SPDX-License-Identifier: Apache-2.0
Name:           tshotkeytrigger
Version:        0.1.0
Release:        1%{?dist}
Summary:        A CLI tool that triggers hotkey actions in Teamspeak 6 via TeamSpeak Remote Applications API.
License:        MIT
URL:            https://github.com/jmansar/tshotkeytrigger
Source0:        tshotkeytrigger-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A CLI tool that triggers hotkey actions in Teamspeak 6 via TeamSpeak Remote Applications API.

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
