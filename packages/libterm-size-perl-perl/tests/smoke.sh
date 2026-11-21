#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libterm-size-perl-perl
python3 - <<'PY'
import fcntl, os, pty, struct, subprocess, termios

master, slave = pty.openpty()
try:
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 41, 97, 970, 410))
    env = os.environ.copy()
    for key in ('PERL5LIB', 'PERLLIB', 'PERL5OPT'):
        env.pop(key, None)
    test = subprocess.run(['/usr/bin/perl', '-MTerm::Size::Perl', '-e', '''
        die "missing real tty\n" unless -t STDIN;
        die "wrong char size\n" unless join("x", Term::Size::Perl::chars(*STDIN)) eq "97x41";
        die "wrong pixel size\n" unless join("x", Term::Size::Perl::pixels(*STDIN)) eq "970x410";
        print "installed real PTY: 97x41 chars; 970x410 pixels\n";
    '''], stdin=slave, capture_output=True, env=env, check=True, timeout=30)
    assert test.stdout == b'installed real PTY: 97x41 chars; 970x410 pixels\n'
    assert not test.stderr
    print(test.stdout.decode(), end='')
finally:
    os.close(slave)
    os.close(master)
PY
