# SPDX-License-Identifier: MIT
Name:           ii
Version:        2.0
Release:        1%{?dist}
Summary:        Minimal FIFO and filesystem based IRC client
License:        MIT AND ISC
URL:            https://tools.suckless.org/ii/
Source0:        ii-2.0.tar.gz
Patch0:         patches/0001-restore-strlcpy-isc-notice.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3


%description
Minimal IRC client controlled through private per-server/channel FIFOs.
TLS, when needed, is provided by an external tunnel as documented upstream.

%package tests
Summary:        Offline private IRC and FIFO functional checks for ii
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Original upstream archive and notices plus deterministic downstream Unix-socket,
loopback TCP, IRC command, log and FIFO cleanup checks. No upstream test target
exists. No public IRC connection or native hardware validation is performed.

%prep
%autosetup -p1
sed -n '1,15p' strlcpy.c > LICENSE.strlcpy
cat > downstream-qa.py <<'II_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
"""Private IRC protocol tests, not external-service or native timing proof."""
import errno
import hashlib
import os
from pathlib import Path
import socket
import stat
import subprocess as S
import sys
import tarfile
import tempfile
import time
root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/ii';checks=[]
archive=root/'usr/share/ii/qa/ii-2.0.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='4f67afcd208c07939b88aadbf21497a702ad0a07f9b5a6ce861f9f39ffe5425b'
with tarfile.open(archive,'r:gz')as tf:
    original={m.name:tf.extractfile(m).read()for m in tf.getmembers()if m.isfile()}
assert len(original)==8
for name in ('ii','ii-tests'):
    assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==original['ii-2.0/LICENSE']
    notice=(root/'usr/share/licenses'/name/'LICENSE.strlcpy').read_bytes()
    assert b'Copyright (c) 1998 Todd C. Miller <Todd.Miller@courtesan.com>'in notice
    assert b'copyright notice and this permission notice appear in all copies.'in notice
    assert b'OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.'in notice
for name in ('README','FAQ','LICENSE'):
    assert(root/'usr/share/doc/ii'/name).read_bytes()==original['ii-2.0/'+name]
checks.append('original-eight-member-archive-and-all-notices')
env=dict(os.environ,LC_ALL='C',II_TEST_PASS='synthetic-fixture-not-a-secret')
def wait_for(test,detail):
    deadline=time.monotonic()+15
    while time.monotonic()<deadline:
        value=test()
        if value:return value
        time.sleep(0.02)
    raise AssertionError(detail)
def cli(args,needle):
    p=S.run([str(binary),*args],env=env,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==1 and not p.stdout and needle in p.stderr,(args,p.returncode,p.stdout,p.stderr)
    return p
for args in ([],['-v'],['-s']):cli(args,b'usage: '+str(binary).encode()+b' -s host')
checks.append('original-usage-and-required-host-errors')
with tempfile.TemporaryDirectory(prefix='ii-qa-',dir='/tmp')as td:
    base=Path(td)
    cli(['-s','fixture','-u',str(base/'absent')],b': connect: ')
    cli(['-s','fixture','-u',str(base/('x'*120))],b'UNIX domain socket path truncation')
    cli(['-s','127.0.0.1','-p','not-a-port','-i',str(base/'bad-port')],b': getaddrinfo: ')
    assert not(base/'bad-port').exists()
    checks.append('missing-unix-socket-path-boundary-and-numeric-service-errors')
    def exercise(transport,signal_exit=False):
        case=base/(transport+('-signal'if signal_exit else ''));case.mkdir()
        server=socket.socket(socket.AF_UNIX if transport=='unix'else socket.AF_INET,socket.SOCK_STREAM)
        proc=None;peer=None;writers=[];out=None;err=None
        try:
            if transport=='unix':
                address=str(case/'server.sock');server.bind(address);host='fixture';connection=['-u',address]
            else:
                server.bind(('127.0.0.1',0));host='127.0.0.1';connection=['-p',str(server.getsockname()[1])]
            server.listen(1);server.settimeout(15)
            out=open(case/'stdout','wb');err=open(case/'stderr','wb')
            proc=S.Popen([str(binary),'-s',host,*connection,'-i',str(case/'irc'),'-n','ci','-f','Fixture User','-k','II_TEST_PASS'],env=env,stdout=out,stderr=err)
            peer,_=server.accept();peer.settimeout(15);pending=bytearray();lines=[]
            def expect(wanted):
                while b'\n'not in pending:
                    data=peer.recv(4096);assert data,'unexpected client EOF';pending.extend(data)
                line,_,tail=pending.partition(b'\n');pending[:]=tail
                actual=bytes(line)+b'\n';lines.append(actual)
                assert actual==wanted,(transport,wanted,actual,lines)
            expect(b'PASS synthetic-fixture-not-a-secret\r\n');expect(b'NICK ci\r\n')
            expect(('USER ci localhost '+host+' :Fixture User\r\n').encode())
            home=case/'irc'/host;master=home/'in'
            def fifo(path):
                wait_for(path.exists,'missing FIFO '+str(path));mode=path.stat().st_mode
                assert stat.S_ISFIFO(mode)and stat.S_IMODE(mode)==0o700,(path,oct(mode))
            def write(path,line):
                fifo(path)
                def opened():
                    try:return os.open(path,os.O_WRONLY|os.O_NONBLOCK)
                    except OSError as ex:
                        if ex.errno==errno.ENXIO:return None
                        raise
                fd=wait_for(opened,'no FIFO reader '+str(path))
                try:assert os.write(fd,line.encode()+b'\n')==len(line.encode())+1
                finally:os.close(fd)
            def logged(path,text):
                wait_for(lambda:path.exists()and text in path.read_text(),'missing log '+text)
            fifo(master)
            assert stat.S_IMODE(home.stat().st_mode)==0o700
            peer.sendall(b':server 001 ci :Welcome fixture\r\nPING :private-fixture\r\n')
            expect(b'PONG private-fixture\r\n');logged(home/'out','Welcome fixture')
            write(master,'/j #qa secret-key');expect(b'JOIN #qa secret-key\r\n');channel=home/'#qa';fifo(channel/'in')
            peer.sendall(b':ci!u@h JOIN :#qa\r\n:peer!u@h PRIVMSG #qa :incoming channel\r\n')
            logged(channel/'out','ci(u@h) has joined #qa');logged(channel/'out','<peer> incoming channel')
            write(channel/'in','outgoing channel');expect(b'PRIVMSG #qa :outgoing channel\r\n');logged(channel/'out','<ci> outgoing channel')
            write(channel/'in','/t fixture topic');expect(b'TOPIC #qa :fixture topic\r\n')
            peer.sendall(b':peer!u@h TOPIC #qa :new topic\r\n');logged(channel/'out','peer changed topic to "new topic"')
            write(master,'/a away reason');expect(b'AWAY :away reason\r\n');logged(home/'out','ci is away "away reason"')
            write(master,'/a');expect(b'AWAY\r\n')
            write(master,'/n ci2');expect(b'NICK ci2\r\n');peer.sendall(b':ci!u@h NICK :ci2\r\n');logged(home/'out','changed nick to "ci2"')
            peer.sendall(b':peer!u@h PRIVMSG ci2 :incoming private\r\n');query=home/'peer';fifo(query/'in');logged(query/'out','<peer> incoming private')
            write(query/'in','outgoing private');expect(b'PRIVMSG peer :outgoing private\r\n');logged(query/'out','<ci2> outgoing private')
            write(master,'/j buddy hello buddy');expect(b'PRIVMSG buddy :hello buddy\r\n');fifo(home/'buddy/in');logged(home/'buddy/out','<ci2> hello buddy')
            write(master,'/WHO #qa');expect(b'WHO #qa\r\n')
            write(channel/'in','/l fixture-part');expect(b'PART #qa :fixture-part\r\n')
            wait_for(lambda:not(channel/'in').exists(),'PART did not remove input FIFO')
            if signal_exit:
                proc.terminate()
            else:
                write(master,'/q fixture-finished');expect(b'QUIT :fixture-finished\r\n')
            assert proc.wait(timeout=15)==0
            assert not list(home.rglob('in')),'input FIFOs remained after client cleanup'
            out.close();out=None;err.close();err=None
            assert not(case/'stderr').read_bytes(),(case/'stderr').read_bytes()
            assert (case/'stdout').read_bytes()
            print('II_CASE_OK '+transport+('-signal'if signal_exit else '-quit')+' '+str(len(lines)))
        finally:
            if proc and proc.poll()is None:
                proc.terminate()
                try:proc.wait(timeout=5)
                except S.TimeoutExpired:proc.kill();proc.wait(timeout=5)
            if peer:peer.close()
            server.close()
            if out:out.close()
            if err:err.close()
    exercise('unix');checks.append('private-unix-irc-all-commands-logs-and-quit-cleanup')
    exercise('tcp');checks.append('numeric-loopback-tcp-all-commands-logs-and-quit-cleanup')
    exercise('unix',True);checks.append('private-unix-term-cleanup')
print('II_QA_OK '+str(len(checks))+' '+','.join(checks))
II_QA

%build
# Original default all target, system flags and bundled strlcpy fallback retained.
%make_build CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" PREFIX=%{_prefix} MANPREFIX=%{_mandir} DOCPREFIX=%{_docdir}

%install
%make_install CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" PREFIX=%{_prefix} MANPREFIX=%{_mandir} DOCPREFIX=%{_docdir}
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE.strlcpy %{buildroot}%{_licensedir}/%{name}/LICENSE.strlcpy
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 LICENSE.strlcpy %{buildroot}%{_licensedir}/%{name}-tests/LICENSE.strlcpy
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# Upstream declares no check/test target; mandatory fixtures add coverage.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/LICENSE.strlcpy
%doc %{_docdir}/%{name}
%{_bindir}/ii
%{_mandir}/man1/ii.1*

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%license %{_licensedir}/%{name}-tests/LICENSE.strlcpy
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Mon Oct 19 2026 yinjiayi <noreply@users.noreply.github.com> - 2.0-1
- Preserve original default build/install and restore bundled ISC notice.
- Require isolated Unix/TCP IRC, log, command, permission and cleanup fixtures.
