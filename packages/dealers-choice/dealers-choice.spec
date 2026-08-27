# SPDX-License-Identifier: Apache-2.0
Name:           dealers-choice
Version:        0.0.15
Release:        1%{?dist}
Summary:        Online Multiplayer Stud and Draw Poker, Texas Hold'em and Omaha
License:        MIT
URL:            https://github.com/Dealer-s-Choice/dealers-choice
Source0:        dealers-choice-0.0.15.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Online Multiplayer Stud and Draw Poker, Texas Hold'em and Omaha

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
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.15-1
- Initial openEuler RISC-V package from the full package inventory.
