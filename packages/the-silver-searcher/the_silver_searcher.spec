# SPDX-License-Identifier: Apache-2.0
Name:           the_silver_searcher
Version:        2.2.0
Release:        1%{?dist}
Summary:        Fast recursive code-searching tool
License:        Apache-2.0 AND BSD-1-Clause
URL:            https://github.com/ggreer/the_silver_searcher
Source0:        the_silver_searcher-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcre-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
The Silver Searcher, commonly invoked as ag, recursively searches source
trees while honoring common version-control ignore files. It supports PCRE
patterns, compressed input, file-type filters, and parallel traversal.

%prep
%autosetup -p1 -n the_silver_searcher-%{version}

%build
autoreconf --force --install
%configure
%make_build

%install
%make_install

%check
./ag --version | grep -F 'ag version 2.2.0'
check_dir=$(mktemp -d)
trap 'rm -rf -- "$check_dir"' EXIT
printf '%s\n' 'alpha' 'needle from file' >"$check_dir/input.txt"
./ag --noaffinity --nocolor --nogroup --workers=1 --parallel \
  'needle' "$check_dir" | grep -F 'needle from file'
printf '%s\n' 'alpha' 'needle from stdin' | \
  ./ag --noaffinity --nocolor --workers=1 --parallel 'needle' - | \
  grep -Fx 'needle from stdin'

%files
%license LICENSE
%doc NOTICE README.md
%{_bindir}/ag
%{_mandir}/man1/ag.1*
%{_datadir}/the_silver_searcher/
%{_datadir}/zsh/site-functions/_the_silver_searcher

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-1
- Package the official stable 2.2.0 tag for RVA23.
- Exercise deterministic file and stdin searches during check and smoke.
