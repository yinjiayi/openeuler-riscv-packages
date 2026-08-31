# SPDX-License-Identifier: Apache-2.0
Name:           bmon
Version:        4.0
Release:        1%{?dist}
Summary:        Portable bandwidth monitor and rate estimator
License:        MIT AND BSD-2-Clause
URL:            https://github.com/tgraf/bmon
Source0:        bmon-4.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libconfuse-devel
BuildRequires:  libnl3-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config


%description
Portable bandwidth monitor and rate estimator

%prep
%autosetup -p1 -n bmon-%{version}

%build
%configure
%make_build

%install
%make_install
install -Dpm0644 LICENSE.BSD %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.BSD
install -Dpm0644 LICENSE.MIT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.MIT

%check
./src/bmon -V | grep -F 'bmon 4.0'
./src/bmon -h | grep -F 'Usage: bmon'

%files
%license %{_datadir}/licenses/%{name}/LICENSE.BSD
%license %{_datadir}/licenses/%{name}/LICENSE.MIT
%doc README.md NEWS
%{_bindir}/bmon
%{_docdir}/%{name}/examples/bmon.conf
%{_mandir}/man8/bmon.8*

%changelog
* Sat Aug 22 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-1
- Package upstream bmon with explicit licenses and CLI checks.
