# SPDX-License-Identifier: Apache-2.0
Name:           xtrans
Version:        1.6.0
Release:        1%{?dist}
Summary:        Shared X.Org network transport source and headers
License:        HPND AND HPND-sell-variant AND MIT AND MIT-open-group AND X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libxtrans
Source0:        xtrans-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  make
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description
xtrans supplies common network transport source and headers that X.Org
components compile into their own libraries or servers. It is not a shared
library.

%prep
%autosetup -p1

%build
%configure --disable-docs
%make_build

%install
%make_install

%check
# Upstream registers no test programs; retain its check target.
%make_build check

%files
%license COPYING
%doc README.md doc/xtrans.xml
%{_includedir}/X11/Xtrans/Xtrans.h
%{_includedir}/X11/Xtrans/Xtrans.c
%{_includedir}/X11/Xtrans/Xtransint.h
%{_includedir}/X11/Xtrans/Xtranslcl.c
%{_includedir}/X11/Xtrans/Xtranssock.c
%{_includedir}/X11/Xtrans/Xtransutil.c
%{_includedir}/X11/Xtrans/transport.c
%{_datadir}/aclocal/xtrans.m4
%{_datadir}/pkgconfig/xtrans.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Package official X.Org 1.6.0 shared transport sources and headers.
