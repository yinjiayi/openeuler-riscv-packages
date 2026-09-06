# SPDX-License-Identifier: Apache-2.0
Name:           hexchat-otr
Version:        0.2.2
Release:        1%{?dist}
Summary:        HexChat plugin for Off-The-Record support
License:        GPL-2.0-or-later
URL:            https://github.com/TingPing/hexchat-otr
Source0:        hexchat-otr-0.2.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
HexChat plugin for Off-The-Record support

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
