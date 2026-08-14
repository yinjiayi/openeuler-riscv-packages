# SPDX-License-Identifier: Apache-2.0
Name:           nudoku
Version:        8.0.1
Release:        1%{?dist}
Summary:        Ncurses Sudoku game for the terminal
License:        GPL-3.0-only
URL:            https://github.com/jubalh/nudoku
Source0:        nudoku-8.0.1.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig

%description
nudoku is a Sudoku game and solver with an ncurses terminal interface.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-cairo
%make_build

%install
%make_install
%find_lang %{name}

%check
./src/nudoku -v | grep -F '%{version}'

%files -f %{name}.lang
%license LICENSE
%doc AUTHORS ChangeLog README.md
%{_bindir}/nudoku
%{_mandir}/man6/nudoku.6*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.0.1-1
- Initial openEuler RISC-V package.

