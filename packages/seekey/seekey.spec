# SPDX-License-Identifier: Apache-2.0
Name:           seekey
Version:        0.2.1
Release:        2%{?dist}
Summary:        Wayland keyboard visualizer with floating key bubbles
License:        MIT
URL:            https://github.com/Nakanomk/Seekey
Source0:        seekey-0.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  gtk4-layer-shell
BuildRequires:  json-glib-devel
BuildRequires:  libevdev-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config

%description
Wayland keyboard visualizer with floating key bubbles

%prep
%autosetup -n Seekey-%{version} -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-2
- Match the case-sensitive source archive root.
- Declare the translation and pkg-config development providers used by the Makefile.
- Run the upstream check target that builds and executes the bundled unit tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
