#!/usr/bin/python3
# SPDX-License-Identifier: MIT
"""Offline CLI and bounded pseudoterminal checks, not native terminal proof."""
import errno
import fcntl
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time

root = Path(sys.argv[1] or '/')
binary = root / 'usr/bin/hyx'
env = dict(os.environ, LC_ALL='C', TERM='xterm')
q = subprocess.run([str(binary), '--version'], env=env, capture_output=True, timeout=30)
assert q.returncode == 0 and q.stdout == b'This is hyx version 2026.01.11.\n', q
q = subprocess.run([str(binary), '--help'], env=env, capture_output=True, timeout=30)
assert q.returncode == 0 and b'hex editor' in q.stdout and b'undo' in q.stdout, q
q = subprocess.run([str(binary), '--invalid-option'], env=env, capture_output=True, timeout=30)
assert q.returncode != 0 and b'invocation' in q.stdout, q


def check(name, initial, keys, expected, size=(24, 80), unnamed=False):
    with tempfile.TemporaryDirectory(prefix='hyx-check-') as work:
        path = Path(work) / 'fixture.bin'
        if not unnamed:
            path.write_bytes(initial)
        pid, master = pty.fork()
        if not pid:
            fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', *size, 0, 0))
            os.chdir(work)
            os.execve(str(binary), [str(binary)] + ([] if unnamed else [str(path)]), env)
        transcript = bytearray()
        sent = False
        status = None
        deadline = time.monotonic() + 30
        try:
            fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack('HHHH', *size, 0, 0))
            while time.monotonic() < deadline:
                ready, _, _ = select.select([master], [], [], 0.05)
                if ready:
                    try:
                        data = os.read(master, 65536)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                        data = b''
                    transcript.extend(data)
                    assert len(transcript) < 1024 * 1024, name
                    if not sent and b'|' in transcript:
                        os.write(master, keys)
                        sent = True
                done, status_now = os.waitpid(pid, os.WNOHANG)
                if done:
                    status = status_now
                    break
            assert sent and status is not None, (name, 'timeout', bytes(transcript[-1024:]))
            assert os.waitstatus_to_exitcode(status) == 0, (name, status, bytes(transcript[-1024:]))
            attrs = termios.tcgetattr(master)
            assert attrs[3] & termios.ECHO and attrs[3] & termios.ICANON, name
            if expected is not None:
                assert path.read_bytes() == expected, name
            print('PASS', name, flush=True)
        finally:
            if status is None:
                os.kill(pid, signal.SIGKILL)
                os.waitpid(pid, 0)
            os.close(master)


check('replace-save', b'ABC', b'00:wq\n', b'\x00BC')
check('undo-redo-save', b'ABC', b'00u\x12:wq\n', b'\x00BC')
check('empty-info', b'', b'\x07q', b'')
check('new-insert-save', b'', b'\x07\tZ\t:wq fixture.bin\n', b'Z', unnamed=True)
check('search-next', b'ABCABC', b'/x 4142\nn:wq\n', b'ABCABC')
check('ascii-special-key', b'ABC', b'\t\x1b[C\tq', b'ABC')
check('command-special-key', b'ABC', b':\x1b[Aq\n', b'ABC')
check('narrow-empty-info', b'', b'\x07q', b'', size=(1, 1))
print('PASS hyx offline CLI and 8 PTY cases')
