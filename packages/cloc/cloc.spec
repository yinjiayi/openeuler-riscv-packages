# SPDX-License-Identifier: Apache-2.0
Name:           cloc
Version:        2.10
Release:        1%{?dist}
Summary:        Count lines of code in many programming languages
License:        GPL-2.0-or-later
URL:            https://github.com/AlDanial/cloc
Source0:        cloc-2.10.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-Parallel-ForkManager
BuildRequires:  perl-Regexp-Common
BuildRequires:  perl-interpreter
Requires:       perl-interpreter
Requires:       perl-Parallel-ForkManager
Requires:       perl-Regexp-Common

%description
Count lines of code in many programming languages

%prep
%autosetup -p1 -n cloc-%{version}

%build
# cloc is a Perl script; the upstream Unix Makefile owns installation.

%install
%make_install -C Unix PREFIX=%{_prefix}

%check
make -C Unix test

%files
%license LICENSE Unix/COPYING
%doc README.md
%{_bindir}/cloc
%{_mandir}/man1/cloc.1*

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.10-1
- Package the official cloc 2.10 release for openEuler RISC-V.
- Install from the upstream Unix Makefile and retain its complete test suite.
