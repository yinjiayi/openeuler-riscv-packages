# SPDX-License-Identifier: Apache-2.0

Name:           bmake
Version:        20260714
Release:        1%{?dist}
Summary:        Portable version of the NetBSD make build tool
License:        BSD-3-Clause AND BSD-2-Clause AND BSD-4-Clause-UC
URL:            https://www.crufty.net/help/sjg/bmake.htm
Source0:        bmake-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  ksh
BuildRequires:  lua
BuildRequires:  sed
BuildRequires:  tcsh
BuildRequires:  util-linux
BuildRequires:  which
Requires:       mk-files = %{version}-%{release}

%description
Bmake is a portable version of the NetBSD make tool. It reads dependency rules,
determines which targets are out of date, and executes the commands needed to
update them. Its language includes the advanced features used by NetBSD and
portable BSD-style build systems.

%package -n mk-files
Summary:        Portable makefile infrastructure for bmake
BuildArch:      noarch
Requires:       python3

%description -n mk-files
Portable BSD-style makefiles and helper scripts used by bmake to build
programs, libraries, documentation, and recursive source trees.

%prep
%autosetup -n bmake -p1

# The installed helper supports Python 3, but upstream's generic interpreter
# name has no provider on the target. Keep the source logic unchanged.
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/python3|' mk/meta2deps.py

%build
unset MAKEFLAGS MAKEOBJDIR MAKEOBJDIRPREFIX MAKESYSPATH
CFLAGS="%{optflags}" \
LDFLAGS="%{build_ldflags}" \
./boot-strap \
  -o Linux \
  --prefix=%{_prefix} \
  --with-default-sys-path=%{_datadir}/mk \
  --without-filemon \
  op=build

%install
unset MAKEFLAGS MAKEOBJDIR MAKEOBJDIRPREFIX MAKESYSPATH
./boot-strap \
  -o Linux \
  --prefix=%{_prefix} \
  --with-default-sys-path=%{_datadir}/mk \
  --without-filemon \
  --install-prefix=%{_prefix} \
  --install-destdir=%{buildroot} \
  STRIP_FLAG= \
  op=install

%check
unset MAKEFLAGS MAKEOBJDIR MAKEOBJDIRPREFIX MAKESYSPATH
./boot-strap -o Linux op=test

%files
%license LICENSE
%doc ChangeLog README
%{_bindir}/bmake
%{_mandir}/man1/bmake.1*

%files -n mk-files
%license LICENSE
%doc mk/README mk/mk-files.txt
%{_datadir}/mk/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20260714-1
- Initial openEuler RISC-V package with the complete upstream unit suite.
