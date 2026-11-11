# SPDX-License-Identifier: MIT
Name:           sselp
Version:        0.2
Release:        1%{?dist}
Summary:        Simple X11 PRIMARY selection printer
License:        MIT
URL:            https://tools.suckless.org/x/sselp/
Source0:        sselp-0.2.tar.gz
Patch0:         patches/0001-correct-property-chunk-offset-and-validation.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  libX11-devel
BuildRequires:  python3
BuildRequires:  xorg-x11-server-Xvfb

%description
Print the X11 PRIMARY selection as UTF-8, followed by a newline when nonempty.

%package tests
Summary:        Offline private-Xvfb protocol fixtures for sselp
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb

%description tests
Original source, MIT notices and downstream selection/property boundary checks.
These are isolated protocol fixtures, not native desktop or full ICCCM proof.

%prep
%setup -q
%patch0 -p1
cat > downstream-qa.py <<'SSELP_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
"""Offline protocol fixtures, not native desktop/input or full ICCCM validation."""
import ctypes as C
import ctypes.util
import hashlib
import os
from pathlib import Path
import select
import subprocess as S
import sys
import tarfile
import tempfile
import time

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/sselp';checks=[]
env=dict(os.environ,LC_ALL='C',DISPLAY='')
archive=root/'usr/share/sselp/qa/sselp-0.2.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='cd0f95ec0eb571a6dd3c48ba3aa931080eb33bc81805bd72832cc04c01b8b822'
with tarfile.open(archive,'r:gz')as tf:
    original={m.name:tf.extractfile(m).read()for m in tf.getmembers()if m.isfile()}
assert len(original)==5
license_=original['sselp-0.2/LICENSE']
assert b'Anselm R Garbe'in license_ and b'Permission is hereby granted'in license_
for name in ('sselp','sselp-tests'):
    assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==license_
assert(root/'usr/share/doc/sselp/README').read_bytes()==original['sselp-0.2/README']
checks.append('original-five-member-archive-and-license')
def run(args=()):
    p=S.run([str(binary),*args],env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=20)
    assert p.returncode==0 and not p.stderr,(args,p.returncode,p.stdout,p.stderr)
    return p.stdout
assert run(['-v'])=='sselp-0.2, © 2006-2008 Anselm R Garbe\n'.encode()
checks.append('original-version-without-display')
assert run()==b'';checks.append('original-no-display-empty-success')
x=C.CDLL(ctypes.util.find_library('X11'))
def proto(name,result,*args):
    f=getattr(x,name);f.restype=result;f.argtypes=list(args);return f
class Request(C.Structure):
    _fields_=[('type',C.c_int),('serial',C.c_ulong),('send_event',C.c_int),('display',C.c_void_p),('owner',C.c_ulong),('requestor',C.c_ulong),('selection',C.c_ulong),('target',C.c_ulong),('property',C.c_ulong),('time',C.c_ulong)]
class Notify(C.Structure):
    _fields_=[('type',C.c_int),('serial',C.c_ulong),('send_event',C.c_int),('display',C.c_void_p),('requestor',C.c_ulong),('selection',C.c_ulong),('target',C.c_ulong),('property',C.c_ulong),('time',C.c_ulong)]
class Event(C.Union):
    _fields_=[('type',C.c_int),('request',Request),('selection',Notify),('pad',C.c_long*24)]
assert C.sizeof(Event)==24*C.sizeof(C.c_long)
op=proto('XOpenDisplay',C.c_void_p,C.c_char_p);close=proto('XCloseDisplay',C.c_int,C.c_void_p)
sync=proto('XSync',C.c_int,C.c_void_p,C.c_int);rootwin=proto('XDefaultRootWindow',C.c_ulong,C.c_void_p)
intern=proto('XInternAtom',C.c_ulong,C.c_void_p,C.c_char_p,C.c_int)
create=proto('XCreateSimpleWindow',C.c_ulong,C.c_void_p,C.c_ulong,C.c_int,C.c_int,C.c_uint,C.c_uint,C.c_uint,C.c_ulong,C.c_ulong)
destroy=proto('XDestroyWindow',C.c_int,C.c_void_p,C.c_ulong)
setowner=proto('XSetSelectionOwner',C.c_int,C.c_void_p,C.c_ulong,C.c_ulong,C.c_ulong)
owner=proto('XGetSelectionOwner',C.c_ulong,C.c_void_p,C.c_ulong)
pending=proto('XPending',C.c_int,C.c_void_p);nextevent=proto('XNextEvent',C.c_int,C.c_void_p,C.POINTER(Event))
change=proto('XChangeProperty',C.c_int,C.c_void_p,C.c_ulong,C.c_ulong,C.c_ulong,C.c_int,C.c_int,C.POINTER(C.c_ubyte),C.c_int)
send=proto('XSendEvent',C.c_int,C.c_void_p,C.c_ulong,C.c_int,C.c_long,C.POINTER(Event))
with tempfile.TemporaryDirectory(prefix='sselp-qa-')as temporary:
    env['HOME']=temporary;env['XDG_CACHE_HOME']=temporary
    rd,wr=os.pipe();server=dpy=None;window=0
    try:
        with(Path(temporary)/'xvfb.log').open('wb')as log:
            try:server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=log,stderr=log,env=env)
            finally:os.close(wr)
            assert select.select([rd],[],[],20)[0],'private display allocation timeout'
            number=os.read(rd,64).strip();assert number.isdigit()
            env['DISPLAY']=':'+number.decode();dpy=op(env['DISPLAY'].encode());assert dpy
            primary=intern(dpy,b'PRIMARY',0);utf8=intern(dpy,b'UTF8_STRING',0)
            assert owner(dpy,primary)==0 and run()==b''
            checks.append('no-selection-owner-empty-success')
            window=create(dpy,rootwin(dpy),0,0,10,10,0,0,0);assert window
            setowner(dpy,primary,window,0);sync(dpy,0);assert owner(dpy,primary)==window
            def fixture(data,refuse=False,format_=8):
                requests=0
                with tempfile.TemporaryFile()as out,tempfile.TemporaryFile()as err:
                    p=S.Popen([str(binary)],env=env,stdin=S.DEVNULL,stdout=out,stderr=err)
                    deadline=time.monotonic()+20
                    try:
                        while p.poll()is None:
                            while pending(dpy):
                                ev=Event();nextevent(dpy,C.byref(ev))
                                if ev.type!=30:continue
                                q=ev.request;assert q.owner==window and q.selection==primary and q.target==utf8
                                prop=q.property or q.target
                                if not refuse:
                                    if format_==8:
                                        buf=(C.c_ubyte*max(1,len(data)))();buf[:len(data)]=data;count=len(data)
                                    else:
                                        buf=C.cast((C.c_ulong*1)(17),C.POINTER(C.c_ubyte));count=1
                                    change(dpy,q.requestor,prop,utf8,format_,0,buf,count)
                                answer=Event();answer.selection=Notify(31,0,1,dpy,q.requestor,q.selection,q.target,0 if refuse else prop,q.time)
                                assert send(dpy,q.requestor,0,0,C.byref(answer));sync(dpy,0);requests+=1
                            assert time.monotonic()<deadline,('client completion timeout',len(data),requests)
                            time.sleep(0.005)
                        assert p.returncode==0,p.returncode
                    finally:
                        if p.poll()is None:p.kill()
                        p.wait(timeout=5)
                    out.seek(0);err.seek(0);actual=out.read();error=err.read()
                    assert not error,error
                    return actual,requests
            for label,data in [('empty',b''),('ascii',b'hello'),('utf8','λ 中'.encode()),('embedded-nul',b'a\0b'),('existing-newline',b'x\n'),('chunk-minus-one',b'a'*16383),('one-chunk',b'b'*16384),('chunk-plus-one',b'c'*16385),('two-chunks-plus-one',(b'0123456789abcdef'*2048)+b'\n')]:
                actual,requests=fixture(data);assert actual==data+(b'\n'if data else b''),(label,len(actual),len(data))
                assert requests==max(1,(len(data)+16383)//16384),(label,requests)
                checks.append('selection-'+label)
            assert fixture(b'',refuse=True)==(b'',1)
            checks.append('owner-refuses-conversion-empty-success')
            assert fixture(b'',format_=32)==(b'',1)
            checks.append('unsupported-property-format-no-overread')
    finally:
        if dpy:
            if window:destroy(dpy,window)
            close(dpy)
        os.close(rd)
        if server:
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('SSELP_QA_OK '+str(len(checks))+' '+','.join(checks))
SSELP_QA

%build
# Keep original default all, C99, warnings, -Os, VERSION and libc/Xlib linkage.
# Let normal RPM processing strip/debug-package the binary, not upstream -s.
%make_build all CC=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"

%install
%make_install CC=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 README %{buildroot}%{_docdir}/%{name}/README
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# Upstream has no test/check target; no original test is removed or skipped.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_bindir}/sselp

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.2-1
- Fix property chunk offsets and add offline staged/installed protocol checks.
