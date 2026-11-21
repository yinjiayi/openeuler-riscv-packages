# SPDX-License-Identifier: Apache-2.0
Name:           dte
Version:        1.11.1
Release:        1%{?dist}
Summary:        Small configurable console text editor
License:        GPL-2.0-only
URL:            https://craigbarnes.gitlab.io/dte/
Source0:        dte-1.11.1.tar.gz
Patch0:         0001-preserve-dangling-symlink-targets.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  coreutils
BuildRequires:  gawk
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  util-linux
BuildRequires:  patch

%description
Small configurable console text editor with syntax highlighting, multiple
buffers, command macros and a built-in configuration language.

%prep
%autosetup -p1

%build
%make_build V=1 CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"

%install
make install V=1 CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" \
    prefix=%{_prefix} DESTDIR=%{buildroot}

%check
# Full upstream default check: C unit/integration tests and CLI option tests.
# util-linux supplies setsid for the original Linux no-controlling-tty test.
make check V=1 CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/dte
%{_mandir}/man1/dte.1*
%{_mandir}/man5/dterc.5*
%{_mandir}/man5/dte-syntax.5*
%{_datadir}/bash-completion/completions/dte
%{_datadir}/applications/dte.desktop
%{_datadir}/metainfo/dte.appdata.xml

%changelog
* Fri Nov 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.1-1
- Package the signed upstream release with full default tests.
- Preserve dangling symlink targets with additional regression tests.
