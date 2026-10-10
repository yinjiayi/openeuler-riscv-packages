# SPDX-License-Identifier: Apache-2.0
Name:           irc-otr
Version:        1.0.2
Release:        1%{?dist}
Summary:        Off-The-Record Messaging plugin for irssi
License:        GPL-2.0-or-later
URL:            https://github.com/cryptodotis/irssi-otr
Source0:        irc-otr-1.0.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Off-The-Record Messaging plugin for irssi

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
