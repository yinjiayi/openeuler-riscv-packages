# SPDX-License-Identifier: Apache-2.0
Name:           vibepaper
Version:        0.2.1
Release:        1%{?dist}
Summary:        Wayland wallpaper daemon that generates and refines wallpapers via OpenAI, Gemini, Stability and other image APIs
License:        MIT
URL:            https://github.com/maxischmaxi/vibepaper
Source0:        vibepaper-0.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Wayland wallpaper daemon that generates and refines wallpapers via OpenAI, Gemini, Stability and other image APIs

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
