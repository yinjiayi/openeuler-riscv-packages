# SPDX-License-Identifier: Apache-2.0
Name:           pipewire-module-xrdp
Version:        0.2
Release:        1%{?dist}
Summary:        xrdp pipewire module
License:        MIT
URL:            https://github.com/neutrinolabs/pipewire-module-xrdp
Source0:        pipewire-module-xrdp-0.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
xrdp pipewire module

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Initial openEuler RISC-V package from the full package inventory.
