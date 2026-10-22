# SPDX-License-Identifier: Apache-2.0
Name:           pv
Version:        1.11.0
Release:        3%{?dist}
Summary:        Monitor data through a pipe
License:        GPL-3.0-or-later
URL:            https://www.ivarch.com/programs/pv.shtml
Source0:        pv-%{version}.tar.gz
Patch0:         0001-tests-report-valgrind-log-on-any-failure.patch

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
set +e
HOME="$pv_check_home" SHELL=/bin/sh TERM=xterm %make_build check
pv_check_status=$?
set -e
if [ "$pv_check_status" -ne 0 ]; then
  for pv_check_log in test-suite.log tests/*.log valgrind.out; do
    [ -f "$pv_check_log" ] || continue
    printf '\n===== %s =====\n' "$pv_check_log"
    sed -n '1,2000p' "$pv_check_log"
  done
fi
exit "$pv_check_status"

%files -f %{name}.lang
%license docs/COPYING
%doc README.md docs/ACKNOWLEDGEMENTS.md docs/NEWS.md
%{_bindir}/pv
%{_mandir}/man1/pv.1*

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.0-3
- Retain bounded Valgrind diagnostics for every nonzero wrapper result while
  preserving the complete test suite and its real failure status.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.0-2
- Preserve every upstream check and emit bounded per-test and Valgrind logs when
  the suite fails, so the five QEMU memory-safety failures can be diagnosed.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.0-1
- Update pv for openEuler RISC-V with all upstream terminal and valgrind checks.
