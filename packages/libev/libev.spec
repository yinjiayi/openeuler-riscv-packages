# SPDX-License-Identifier: Apache-2.0
Name:           libev
Version:        4.33
Release:        1%{?dist}
Summary:        High-performance event loop library
License:        BSD-2-Clause OR GPL-2.0-or-later
URL:            https://software.schmorp.de/pkg/libev.html
Source0:        libev-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libev provides a small, high-performance event loop with timers and I/O,
signal, child, and filesystem watchers.

%package devel
Summary:        Headers and linker name for libev
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The C and C++ headers and unversioned shared-library link for applications
using the libev API.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check
# The upstream tarball has no executable tests, so exercise a real timer.
cat > api-check.c <<'EOF'
#include <ev.h>
#include <unistd.h>

static int fired;

static void on_timer(EV_P_ ev_timer *watcher, int revents) {
  (void)watcher;
  if (revents & EV_TIMER)
    fired = 1;
}

int main(void) {
  struct ev_loop *loop = ev_loop_new(EVFLAG_AUTO);
  ev_timer timer;
  if (!loop || ev_version_major() != 4 || ev_version_minor() != 33)
    return 1;
  ev_timer_init(&timer, on_timer, 0.01, 0.0);
  ev_timer_start(loop, &timer);
  for (int i = 0; i < 500 && !fired; ++i) {
    ev_run(loop, EVRUN_NOWAIT);
    usleep(10000);
  }
  ev_timer_stop(loop, &timer);
  ev_loop_destroy(loop);
  return fired ? 0 : 1;
}
EOF
%{__cc} %{build_cflags} -I. api-check.c -L.libs -Wl,-rpath,$PWD/.libs -lev %{build_ldflags} -o api-check
./api-check

%files
%license LICENSE
%doc Changes README
%{_libdir}/libev.so.4*
%{_mandir}/man3/ev.3*

%files devel
%license LICENSE
%{_includedir}/ev.h
%{_includedir}/ev++.h
%{_includedir}/event.h
%{_libdir}/libev.so

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.33-1
- Initial package from the official stable release with event-loop checks.
