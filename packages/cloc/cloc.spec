# SPDX-License-Identifier: Apache-2.0
Name:           cloc
Version:        2.10
Release:        1%{?dist}
Summary:        Count lines of code in many programming languages
License:        GPL-2.0-or-later
URL:            https://github.com/AlDanial/cloc
Source0:        cloc-2.10.tar.gz
Source1:        cloc_submodule_test-f647093e8be34e337366457005cfb8056b847ebb.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  git
BuildRequires:  perl-Parallel-ForkManager
BuildRequires:  perl-Regexp-Common
BuildRequires:  perl-interpreter
Requires:       perl-interpreter
Requires:       perl-Parallel-ForkManager
Requires:       perl-Regexp-Common

%description
Count lines of code in many programming languages

%prep
%autosetup -p1 -n cloc-%{version} -a 1
mv cloc_submodule_test-f647093e8be34e337366457005cfb8056b847ebb \
  Unix/cloc_submodule_test
# Restore the fixture's pinned history because the source archive omits .git.
git -C Unix/cloc_submodule_test init --quiet
git -C Unix/cloc_submodule_test remote add origin \
  https://github.com/AlDanial/cloc_submodule_test.git
git -C Unix/cloc_submodule_test fetch --no-tags --quiet origin \
  f647093e8be34e337366457005cfb8056b847ebb
git -C Unix/cloc_submodule_test reset --quiet --hard \
  f647093e8be34e337366457005cfb8056b847ebb

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
