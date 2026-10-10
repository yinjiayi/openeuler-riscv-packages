# SPDX-License-Identifier: Apache-2.0
Name:           networkmanager-l2tp
Version:        1.52.2
Release:        1%{?dist}
Summary:        NetworkManager VPN plugin for L2TP (with GUI)
License:        GPL-2.0-or-later
URL:            https://github.com/nm-l2tp/NetworkManager-l2tp
Source0:        networkmanager-l2tp-1.52.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
NetworkManager VPN plugin for L2TP (with GUI)

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
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.52.2-1
- Initial openEuler RISC-V package from the full package inventory.
