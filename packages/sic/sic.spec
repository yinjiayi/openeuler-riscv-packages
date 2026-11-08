# SPDX-License-Identifier: Apache-2.0
Name:           sic
Version:        1.3
Release:        1%{?dist}
Summary:        Simple line-oriented IRC client
License:        MIT AND ISC
URL:            https://tools.suckless.org/sic/
Source0:        sic-1.3.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  python3


%description
Small line-oriented IRC client preserving the entire upstream default build,
configuration and channel/server commands. Build/check use no external service.

%package tests
Summary:        Offline protocol checks for sic
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Added downstream functional checks using a private loopback mock IRC server.
Upstream 1.3 has no test target. No native timing or network-security claim.

%prep
%autosetup -n sic-%{version}
# Add only a downstream checker; all nine upstream release files stay intact.
cat > downstream-check.py <<'SIC_CHECK'
# SPDX-License-Identifier: MIT
# Original downstream functional checks; no external IRC server is contacted.
import os
import pathlib
import socket
import subprocess
import sys

assert not sys.flags.optimize
binary = str(pathlib.Path(sys.argv[1]).resolve(strict=True))
assert os.access(binary, os.X_OK)
for args, marker in ((['-v'], b'sic-1.3,'), (['-Z'], b'usage: sic ')):
    q = subprocess.run([binary, *args], capture_output=True, timeout=30)
    # Upstream eprint deliberately exits 1 even for the version option.
    assert q.returncode == 1 and marker in q.stderr and not q.stdout, q
print('PASS original version and invalid-option semantics', flush=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    listener.settimeout(30)
    port = str(listener.getsockname()[1])
    child = subprocess.Popen(
        [binary, '-h', '127.0.0.1', '-p', port, '-n', 'testnick',
         '-k', 'offline-test-password'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        conn, address = listener.accept()
        assert address[0] == '127.0.0.1'
        with conn:
            conn.settimeout(30)
            with conn.makefile('rb') as stream:
                def line():
                    value = stream.readline(8192)
                    assert value.endswith(b'\r\n') and len(value) < 8192, value
                    return value
                assert line() == b'PASS offline-test-password\r\n'
                assert line() == b'NICK testnick\r\n'
                assert line() == b'USER testnick localhost 127.0.0.1 :testnick\r\n'
                print('PASS PASS/NICK/USER handshake', flush=True)
                conn.sendall(b'PING :offline-probe\r\n')
                assert line() == b'PONG offline-probe\r\n'
                conn.sendall(b':guest!u@host PRIVMSG #test :server-message\r\n'
                             b':testnick!u@host NICK :renamed\r\n'
                             b'PING :nick-barrier\r\n')
                assert line() == b'PONG nick-barrier\r\n'
                print('PASS server PING, message and nickname handling', flush=True)
                child.stdin.write(b':j #test\nhello\n:m guest direct\n'
                                  b':s #other\nother-message\n:l #test bye\n'
                                  b':WHO #test\n')
                child.stdin.flush()
                expected = [b'JOIN #test\r\n', b'PRIVMSG #test :hello\r\n',
                            b'PRIVMSG guest :direct\r\n',
                            b'PRIVMSG #other :other-message\r\n',
                            b'PART #test :bye\r\n', b'WHO #test\r\n']
                for value in expected:
                    assert line() == value, value
                print('PASS join, implicit/direct send, channel, part and raw command', flush=True)
            conn.shutdown(socket.SHUT_RDWR)
        out, err = child.communicate(timeout=30)
        assert child.returncode == 1, (child.returncode, out, err)
        assert b'<guest> server-message' in out and b'<renamed> hello' in out
        assert b'<renamed> direct' in out and b'<renamed> other-message' in out
        assert b'remote host closed connection' in err or b'broken pipe' in err
        print('PASS displayed server/self messages and original EOF error', flush=True)
    finally:
        if child.poll() is None:
            child.kill()
            child.communicate(timeout=30)
print('PASS all five downstream functional groups', flush=True)
SIC_CHECK

%build
# Retain upstream all and default features; use distribution hardening flags.
make %{?_smp_mflags} CC='%{__cc}' CFLAGS='%{optflags}' LDFLAGS='%{?build_ldflags}'

%install
make install DESTDIR='%{buildroot}' PREFIX='%{_prefix}' MANPREFIX='%{_mandir}'
install -Dm644 downstream-check.py '%{buildroot}%{_datadir}/sic/qa.py'

%check
# No upstream test/check target exists to skip or replace.
python3 -I -B downstream-check.py ./sic
python3 -I -B '%{buildroot}%{_datadir}/sic/qa.py' '%{buildroot}%{_bindir}/sic'

%files
%license LICENSE strlcpy.c arg.h
%doc README
%{_bindir}/sic
%{_mandir}/man1/sic.1*

%files tests
%license LICENSE strlcpy.c arg.h
%{_datadir}/sic

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Retain default upstream build; add five offline protocol check groups.
