# SPDX-License-Identifier: Apache-2.0
Name:           netlabel-tools
Version:        0.30.0
Release:        1%{?dist}
Summary:        Tools to manage the Linux NetLabel subsystem
License:        GPL-2.0-or-later
URL:            https://github.com/netlabel/netlabel_tools
Source0:        netlabel-tools-0.30.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Tools to manage the Linux NetLabel subsystem

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
%doc README
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.30.0-1
- Initial openEuler RISC-V package from the full package inventory.
