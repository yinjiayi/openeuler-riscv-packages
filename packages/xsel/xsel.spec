# SPDX-License-Identifier: Apache-2.0
Name:           xsel
Version:        1.2.1
Release:        1%{?dist}
Summary:        Command-line access to X11 selections
License:        HPND-sell-variant
URL:            https://vergenet.net/~conrad/software/xsel/
Source0:        xsel-1.2.1.tar.gz
Source1:        GPL-2.0.txt
Patch0:         patches/0001-valid-empty-delete-property-format.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  pkgconfig
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libX11-devel
BuildRequires:  python3
BuildRequires:  xorg-x11-server-Xvfb

%description
XSel reads and writes X11 PRIMARY, SECONDARY and CLIPBOARD selections from
the command line. The original input/output defaults and options are retained.

%package tests
Summary:        Offline private-Xvfb functional checks for xsel
License:        HPND-sell-variant AND X11 AND FSFULLR AND (GPL-2.0-or-later WITH Autoconf-exception-generic)
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb
Requires:       libX11

%description tests
Bounded downstream byte-roundtrip, CLI, default terminal-direction and
selection-clear/delete checks in an isolated Xvfb server. The retained
upstream archive includes auxiliary build-script license notices. These
checks do not certify complete ICCCM, native desktop or security behavior.

%prep
%autosetup -p1
cat > downstream-qa.py <<'XSEL_QA'
# SPDX-License-Identifier: HPND-sell-variant
# Copyright 2026 yinjiayi. Permission to use, copy, modify, distribute and sell
# this software and its documentation for any purpose is granted without fee,
# provided this copyright and permission notice appear in copies and supporting
# documentation. No representations are made about suitability for any purpose.
# It is provided "as is" without express or implied warranty.
"""Bounded private-Xvfb selection roundtrips, not full ICCCM conformance."""
import ctypes as C
import ctypes.util
import gzip
import hashlib
import os
from pathlib import Path
import pty
import select
import subprocess as S
import sys
import tarfile
import tempfile
import time

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/xsel';checks=[]
env=dict(os.environ,LC_ALL='C',DISPLAY='')
archive=root/'usr/share/xsel/qa/xsel-1.2.1.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='18487761f5ca626a036d65ef2db8ad9923bf61685e06e7533676c56d7d60eb14'
with tarfile.open(archive,'r:gz')as tf:
    license_=tf.extractfile('xsel-1.2.1/COPYING').read()
    assert b'Copyright (C) 2001 Conrad Parker' in license_ and b'and sell' in license_
    for name in ('xsel','xsel-tests'):
        assert (root/'usr/share/licenses'/name/'COPYING').read_bytes()==license_
    man=root/'usr/share/man/man1/xsel.1x.gz'
    installed=gzip.decompress(man.read_bytes()) if man.exists() else man.with_suffix('').read_bytes()
    assert installed==tf.extractfile('xsel-1.2.1/xsel.1x').read()
assert hashlib.sha256((root/'usr/share/licenses/xsel-tests/GPL-2.0.txt').read_bytes()).hexdigest()=='edaef632cbb643e4e7a221717a6c441a4c1a7c918e6e4d56debc3d8739b233f6'
checks.append('original-archive-manual-and-licenses')
def run(args,status=0,data=None,stdin=None):
    kwargs=dict(env=env,stdout=S.PIPE,stderr=S.PIPE,timeout=20)
    if data is not None:kwargs['input']=data
    else:kwargs['stdin']=S.DEVNULL if stdin is None else stdin
    p=S.run([str(binary),*args],**kwargs)
    assert p.returncode==status,(args,p.returncode,p.stdout,p.stderr)
    return p
for args in (['--help'],['-h'],['--unknown-qa-option'],['--display'],['--selectionTimeout']):
    p=run(args);assert b'Usage:' in p.stdout and not p.stderr
    checks.append('original-usage-status-'+args[0])
p=run(['--version']);assert p.stdout.startswith(b'xsel version 1.2.1 by ') and not p.stderr
checks.append('version')
p=run(['--output'],1);assert b"Can't open display" in p.stderr
checks.append('no-display-fails')
x=C.CDLL(ctypes.util.find_library('X11'))
def proto(name,result,*args):
    f=getattr(x,name);f.restype=result;f.argtypes=list(args);return f
op=proto('XOpenDisplay',C.c_void_p,C.c_char_p)
close=proto('XCloseDisplay',C.c_int,C.c_void_p)
sync=proto('XSync',C.c_int,C.c_void_p,C.c_int)
atom=proto('XInternAtom',C.c_ulong,C.c_void_p,C.c_char_p,C.c_int)
owner=proto('XGetSelectionOwner',C.c_ulong,C.c_void_p,C.c_ulong)
processes=[]
def stop(p):
    if p.poll() is None:p.terminate()
    try:out,err=p.communicate(timeout=5)
    except S.TimeoutExpired:p.kill();out,err=p.communicate(timeout=5)
    assert not err,dict(owner=getattr(p,'qa_context',{}),pid=p.pid,argv=p.args,returncode=p.returncode,stderr=err,completed_checks=checks)
    return out
with tempfile.TemporaryDirectory(prefix='xsel-qa-')as temporary:
    env['HOME']=temporary;env['XDG_CACHE_HOME']=temporary
    rd,wr=os.pipe()
    with (Path(temporary)/'xvfb.log').open('wb')as log:
        server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=log,stderr=log,env=env)
        os.close(wr);dpy=None
        try:
            assert select.select([rd],[],[],20)[0],'private display allocation timeout'
            number=os.read(rd,64).strip();assert number.isdigit()
            env['DISPLAY']=':'+number.decode();dpy=op(env['DISPLAY'].encode());assert dpy
            atoms={key:atom(dpy,key.encode(),0)for key in ('PRIMARY','SECONDARY','CLIPBOARD','UTF8_STRING')};sync(dpy,0)
            def wait_owner(key,previous,empty=False,p=None):
                deadline=time.monotonic()+20
                while True:
                    current=owner(dpy,atoms[key])
                    if (current==0 if empty else current!=0 and current!=previous):return current
                    assert time.monotonic()<deadline,(key,'ownership timeout',previous,current)
                    assert p is None or p.poll() is None,(key,'owner exited',p.returncode)
                    time.sleep(0.02)
            def write(data,key='PRIMARY',extra=(),implicit=False):
                previous=owner(dpy,atoms[key]);master=slave=pipe_rd=None
                with tempfile.TemporaryFile()as payload:
                    payload.write(data);payload.seek(0)
                    if implicit:
                        assert len(data)<128
                        master,slave=pty.openpty();pipe_rd,pipe_wr=os.pipe()
                        try:assert os.write(pipe_wr,data)==len(data)
                        finally:os.close(pipe_wr)
                    args=['--nodetach','--selectionTimeout','60000',*extra]
                    if not implicit:args+=['--input','--'+key.lower()]
                    p=S.Popen([str(binary),*args],env=env,stdin=pipe_rd if implicit else payload,stdout=slave if implicit else S.PIPE,stderr=S.PIPE)
                    p.qa_context=dict(selection=key,input_bytes=len(data),implicit=implicit)
                    processes.append(p)
                    try:wait_owner(key,previous,p=p)
                    finally:
                        if pipe_rd is not None:os.close(pipe_rd)
                        if slave is not None:os.close(slave)
                        if master is not None:os.close(master)
                return p
            def read(key='PRIMARY',extra=()):
                p=run(['--output','--'+key.lower(),'--selectionTimeout','5000',*extra]);assert not p.stderr,p.stderr
                return p.stdout
            assert read()==b'';checks.append('initial-empty-primary')
            text='primary\ttest\nUTF-8: λ 中\n'.encode()
            write(text);assert read()==text;checks.append('primary-utf8-byte-roundtrip')
            write(b'secondary\n','SECONDARY');write(b'clipboard\n','CLIPBOARD')
            assert read()==text and read('SECONDARY')==b'secondary\n' and read('CLIPBOARD')==b'clipboard\n'
            checks.append('three-independent-selections')
            write(b'append\n',extra=('--append',));assert read()==text+b'append\n'
            checks.append('append-keeps-existing-content')
            write(b'trimmed\n\n',extra=('--trim',));assert read()==b'trimmed\n'
            assert read(extra=('--trim',))==b'trimmed'
            checks.append('trim-input-and-output-one-newline')
            large=(b'0123456789abcdef'*2048)+b'\n'
            write(large);assert read()==large;checks.append('large-incremental-transfer')
            write(b'implicit-input',implicit=True);assert read()==b'implicit-input'
            checks.append('default-stdin-pipe-stdout-tty-input')
            master,slave=pty.openpty()
            try:
                p=run(['--selectionTimeout','5000'],stdin=slave);assert p.stdout==b'implicit-input' and not p.stderr
            finally:os.close(slave);os.close(master)
            checks.append('default-stdin-tty-stdout-pipe-output')
            p=run(['--clear','--primary']);assert not p.stdout and not p.stderr
            wait_owner('PRIMARY',None,empty=True);assert read()==b''
            checks.append('clear-selection')
            delete_owner=write(b'delete-me');p=run(['--delete','--primary','--selectionTimeout','5000'])
            assert not p.stdout and not p.stderr;wait_owner('PRIMARY',None,empty=True);assert read()==b''
            delete_owner.wait(timeout=5);stop(delete_owner);assert delete_owner.returncode==0,delete_owner.returncode
            checks.append('delete-selection-protocol')
            write(b'explicit-display',extra=('--display',env['DISPLAY'],'--name','xsel-downstream-qa'))
            assert read()==b'explicit-display';checks.append('explicit-display-and-window-name')
        finally:
            prior_error=sys.exc_info()[1];cleanup_errors=[]
            for p in reversed(processes):
                try:stop(p)
                except Exception as error:cleanup_errors.append(repr(error))
            if dpy:close(dpy)
            os.close(rd)
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
            assert not cleanup_errors,dict(prior_error=repr(prior_error),owner_errors=cleanup_errors,completed_checks=checks)
print('XSEL_QA_OK '+str(len(checks))+' '+','.join(checks))
XSEL_QA

%build
# The fixed Git tag omits configure and Makefile.in. Regenerate only the
# standard Autotools machinery; configure.ac and Makefile.am stay untouched.
autoreconf -fiv
%configure
%make_build

%install
%make_install
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 COPYING %{buildroot}%{_licensedir}/%{name}/COPYING
install -Dm 0644 COPYING %{buildroot}%{_licensedir}/%{name}-tests/COPYING
install -Dm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}-tests/GPL-2.0.txt

%check
# Keep the original generated Automake check target, even though this release
# declares no TESTS/check_PROGRAMS. Downstream checks supplement, not replace it.
%make_build check
python3 -I -B downstream-qa.py %{buildroot}

%files
%license COPYING
%doc README AUTHORS ChangeLog
%{_bindir}/xsel
%{_mandir}/man1/xsel.1x*

%files tests
%license %{_licensedir}/%{name}-tests/COPYING
%license %{_licensedir}/%{name}-tests/GPL-2.0.txt
%{_libexecdir}/%{name}-tests
%{_datadir}/%{name}/qa

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.2.1-1
- Onboard the fixed official source with unchanged defaults and offline checks.
