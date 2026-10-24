# SPDX-License-Identifier: Apache-2.0
Name:           universal-ctags
Version:        6.2.1
Release:        1%{?dist}
Summary:        Maintained implementation of the ctags source indexer
License:        GPL-2.0-only
URL:            https://ctags.io/
Source0:        universal-ctags-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  grep
BuildRequires:  jansson-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  pcre2-devel
BuildRequires:  perl
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  python3-docutils
BuildRequires:  sed

%description
Universal Ctags generates tag files containing indexes of language objects
found in source files for many programming languages.

%prep
%autosetup -p1

%build
%configure --enable-json --enable-yaml --enable-pcre2 --enable-seccomp
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc README.md NEWS.rst
%{_bindir}/ctags
%{_bindir}/etags
%{_bindir}/optscript
%{_bindir}/readtags

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.2.1-1
- Initial openEuler RISC-V Universal Ctags package with complete tests.
