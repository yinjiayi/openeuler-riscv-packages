# SPDX-License-Identifier: Apache-2.0
Name:           pick
Version:        4.0.0
Release:        1
Summary:        Fuzzy search selection tool for the command line
License:        MIT AND ISC
URL:            https://github.com/mptre/pick
Source0:        pick-4.0.0.tar.gz
Patch0:         0001-bound-incomplete-terminal-escape-sequences.patch
Patch1:         0002-add-offline-installed-default-suite-replay.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  ncurses-base
BuildRequires:  glibc-all-langpacks
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  sed
BuildRequires:  patch
BuildRequires:  findutils


%description
Pick reads choices on standard input and provides interactive fuzzy selection
in a terminal. All upstream selection modes and default tests are retained.

%package tests
Summary:        Unchanged upstream PTY suite for installed pick
Requires:       %{name} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       make
Requires:       ncurses-devel
Requires:       ncurses-base
Requires:       glibc-all-langpacks
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils
Requires:       sed
Requires:       bash
Requires:       findutils

%description tests
Original 31 upstream PTY test files, driver and default test Makefile, replayed
against the installed executable without deleting tests or extending timeouts.
The compiler is used only for original configure probes and the PTY driver.

%prep
%autosetup -n pick-%{version} -p1
# Preserve a pristine patched source tree before generated build outputs exist.
test ! -e ../pick-offline-src
cp -a . ../pick-offline-src

%build
CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" \
    PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir} sh ./configure
%make_build

%install
%make_install
install -d %{buildroot}%{_libexecdir}/pick-tests
tar -C ../pick-offline-src -czf %{buildroot}%{_libexecdir}/pick-tests/source.tar.gz .
install -m 0755 qa/replay.sh %{buildroot}%{_libexecdir}/pick-tests/replay.sh

%check
# Unfiltered upstream default test target: all original 31 .t files.
make test
gcc %{optflags} -I. qa/escape-check.c compat-pledge.o \
    compat-reallocarray.o compat-strtonum.o -lncursesw %{?build_ldflags} -o escape-check
./escape-check
sh %{buildroot}%{_libexecdir}/pick-tests/replay.sh %{buildroot}

%files
%license LICENSE compat-reallocarray.c compat-strtonum.c
%doc README.md CHANGELOG.md
%{_bindir}/pick
%{_mandir}/man1/pick.1*

%files tests
%license LICENSE compat-reallocarray.c compat-strtonum.c
%{_libexecdir}/pick-tests/

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.0-1
- Retain default build, all original tests and MIT/ISC notices; bound incomplete escapes.
