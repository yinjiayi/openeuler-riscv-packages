# SPDX-License-Identifier: Apache-2.0
Name:           booth
Version:        1.2
Release:        1%{?dist}
Summary:        Ticket Manager for Multi-site Clusters
License:        GPL-2.0-or-later
URL:            https://github.com/ClusterLabs/booth
Source0:        booth-1.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Ticket Manager for Multi-site Clusters

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
%doc README
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Initial openEuler RISC-V package from the full package inventory.
