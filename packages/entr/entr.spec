# SPDX-License-Identifier: Apache-2.0
Name: entr
Version: 5.8
Release: 1%{?dist}
Summary: Run arbitrary commands when files change
License: ISC
URL: https://eradman.com/entrproject/
Source0: entr-%{version}.tar.gz
BuildRequires: bash
BuildRequires: file
BuildRequires: gawk
BuildRequires: gcc
BuildRequires: git
BuildRequires: make
BuildRequires: procps-ng
BuildRequires: tmux
BuildRequires: vim-enhanced

%description
entr runs a command whenever one or more watched files change.

%prep
%autosetup -p1

%build
./configure
%make_build

%install
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir}

%check
%make_build check

%files
%license LICENSE
%doc NEWS README.md
%{_bindir}/entr
%{_mandir}/man1/entr.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.8-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
