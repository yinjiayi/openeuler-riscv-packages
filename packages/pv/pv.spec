# SPDX-License-Identifier: Apache-2.0
Name:           pv
Version:        1.11.0
Release:        1%{?dist}
Summary:        Monitor data through a pipe
License:        GPL-3.0-or-later
URL:            https://www.ivarch.com/programs/pv.shtml
Source0:        pv-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  tmux
BuildRequires:  valgrind

%description
pv shows the progress of data moving through a pipeline. It reports elapsed
time, throughput, transferred bytes, completion percentage, and ETA.

%prep
%autosetup -p1 -n pv

%build
autoreconf -vfi
%configure
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/%{name}
%find_lang %{name}

%check
pv_check_home=$(mktemp -d)
trap 'rm -rf -- "$pv_check_home"' EXIT
printf '%s\n' \
  'set-option -g default-shell /bin/sh' \
  'set-option -g default-command "sleep 300"' \
  >"$pv_check_home/.tmux.conf"
HOME="$pv_check_home" SHELL=/bin/sh TERM=xterm %make_build check

%files -f %{name}.lang
%license docs/COPYING
%doc README.md docs/ACKNOWLEDGEMENTS.md docs/NEWS.md
%{_bindir}/pv
%{_mandir}/man1/pv.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.0-1
- Update pv for openEuler RISC-V with all upstream terminal and valgrind checks.
