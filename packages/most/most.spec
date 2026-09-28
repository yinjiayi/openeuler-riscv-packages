# SPDX-License-Identifier: Apache-2.0
Name:           most
Version:        5.2.0
Release:        1%{?dist}
Summary:        Terminal pager with multi-window navigation
License:        GPL-2.0-or-later
URL:            https://www.jedsoft.org/most/
Source0:        most-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  slang-devel

%description
Most is a terminal pager that can display multiple files in split windows and
supports searching, horizontal scrolling, and color output.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
# Upstream ships manual testfiles but has no automated check target. Exercise
# both the built pager's stdin and file paths in non-interactive mode.
most_binary=$(find src -maxdepth 2 -type f -name most -print -quit)
test -n "$most_binary" && test -x "$most_binary"
test "$(printf 'most-stdin-smoke\n' | "$most_binary")" = most-stdin-smoke
printf 'most-file-smoke\n' > most-check-input
test "$("$most_binary" most-check-input)" = most-file-smoke

%files
%license COPYING COPYRIGHT
%{_bindir}/most
%{_mandir}/man1/most.1*
%{_docdir}/most/

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.2.0-1
- Package the official SHA-256-pinned Most 5.2.0 release.
