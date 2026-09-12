# SPDX-License-Identifier: Apache-2.0
Name:           patchutils
Version:        0.4.5
Release:        1%{?dist}
Summary:        Utilities for manipulating patch files
License:        GPL-2.0-or-later
URL:            https://cyberelk.net/tim/software/patchutils/
Source0:        patchutils-%{version}.tar.xz

Requires:       patch

BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pcre2-devel
BuildRequires:  perl-interpreter

%description
patchutils is a collection of command-line programs for inspecting,
filtering, combining, comparing, splitting, and repairing patch files.

%prep
%autosetup -p1

%build
%configure --with-pcre2
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_bindir}/*
%{_datadir}/bash-completion/completions/*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.5-1
- Initial openEuler RISC-V package with PCRE2 and the complete upstream suite.
