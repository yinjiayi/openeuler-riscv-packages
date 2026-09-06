# SPDX-License-Identifier: Apache-2.0
Name:           mactelnet
Version:        0.6.3
Release:        1%{?dist}
Summary:        A linux console tool for connecting to MikroTik RouterOS devices via their ethernet address
License:        GPL-2.0-or-later
URL:            https://github.com/haakonnessjoen/MAC-Telnet
Source0:        mactelnet-0.6.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A linux console tool for connecting to MikroTik RouterOS devices via their ethernet address

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3-1
- Initial openEuler RISC-V package from the full package inventory.
