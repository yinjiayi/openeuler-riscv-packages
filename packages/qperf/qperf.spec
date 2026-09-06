# SPDX-License-Identifier: Apache-2.0
Name:           qperf
Version:        0.4.11
Release:        1%{?dist}
Summary:        OpenFabrics Alliance InfiniBand performance benchmark for bandwidth and latency (supports TCP/IP and RDMA)
License:        GPL-2.0-or-later
URL:            https://github.com/linux-rdma/qperf
Source0:        qperf-0.4.11.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
OpenFabrics Alliance InfiniBand performance benchmark for bandwidth and latency (supports TCP/IP and RDMA)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.11-1
- Initial openEuler RISC-V package from the full package inventory.
