# SPDX-License-Identifier: Apache-2.0
Name:           dosfstools
Version:        4.2
Release:        1%{?dist}
Summary:        Utilities for creating and checking FAT filesystems
License:        GPL-3.0-or-later
URL:            https://github.com/dosfstools/dosfstools
Source0:        dosfstools-4.2.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  mtools
BuildRequires:  pkgconf-pkg-config
BuildRequires:  vim-common

%description
The dosfstools package includes mkfs.fat, fsck.fat, and dosfslabel for
creating and checking MS-DOS FAT filesystems.

%prep
%autosetup -p1

%build
%configure --enable-compat-symlinks
%make_build CFLAGS="%{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing"

%install
%make_install PREFIX="%{_prefix}"
rm -rf %{buildroot}%{_docdir}/%{name}

%check
%make_build check

%files
%license COPYING
%doc NEWS README
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2-1
- Package dosfstools with compatibility links and the complete test suite.
