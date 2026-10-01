# SPDX-License-Identifier: Apache-2.0
Name:           noctalia-greeter
Version:        1.1.0
Release:        1%{?dist}
Summary:        Minimal greetd login greeter with a bundled wlroots compositor
License:        MIT
URL:            https://github.com/noctalia-dev/noctalia-greeter
Source0:        noctalia-greeter-1.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Minimal greetd login greeter with a bundled wlroots compositor

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
