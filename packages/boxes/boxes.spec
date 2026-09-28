# SPDX-License-Identifier: Apache-2.0
Name:           boxes
Version:        2.3.2
Release:        1%{?dist}
Summary:        Draw and remove text boxes using configurable designs
License:        GPL-3.0-only
URL:            https://boxes.thomasjensen.com/
Source0:        boxes-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  bison
BuildRequires:  cmocka-devel
BuildRequires:  diffutils
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libunistring-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel
BuildRequires:  vim-common

%description
boxes is a command-line filter that draws, removes, and edits text boxes
using a collection of configurable ASCII and Unicode designs.

%prep
%autosetup -p1

%build
%make_build build GLOBALCONF=%{_datadir}/boxes CFLAGS_ADDTL="%{optflags}"

%install
install -Dpm0755 out/boxes %{buildroot}%{_bindir}/boxes
install -Dpm0644 boxes-config %{buildroot}%{_datadir}/boxes
install -Dpm0644 doc/boxes.1 %{buildroot}%{_mandir}/man1/boxes.1

%check
# Match all three non-coverage upstream CI suites without skipping cases.
%make_build utest GLOBALCONF=%{_datadir}/boxes
%make_build test-sunny GLOBALCONF=%{_datadir}/boxes
%make_build test GLOBALCONF=%{_datadir}/boxes

%files
%license LICENSE
%doc README.md doc/boxes.el boxes.vim
%{_bindir}/boxes
%{_datadir}/boxes
%{_mandir}/man1/boxes.1*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.2-1
- Package the official SHA-256-pinned boxes 2.3.2 release with all upstream test suites.
