#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libev libev-devel
test -f /usr/include/ev.h
test -f /usr/include/ev++.h

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
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
C

cc "$smoke_dir/smoke.c" -lev -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
