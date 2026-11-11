# SPDX-License-Identifier: MIT
Name:           tabbed
Version:        0.9
Release:        1%{?dist}
Summary:        Generic XEmbed-aware tabbed X11 application container
License:        MIT
URL:            https://tools.suckless.org/tabbed/
Source0:        tabbed-0.9.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3
BuildRequires:  libX11-devel
BuildRequires:  libXft-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  dejavu-sans-mono-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       /bin/sh
Requires:       /usr/bin/xwininfo
Requires:       /usr/bin/xprop
Requires:       /usr/bin/dmenu
Requires:       /usr/bin/grep
Requires:       /usr/bin/sed
Requires:       /usr/bin/xargs

%description
A generic tabbed frontend to XEmbed-aware X11 applications, together with the
original xembed foreground-process command wrapper. Original key bindings and
both default binaries are preserved.

%package tests
Summary:        Offline private-Xvfb and PTY functional checks for tabbed
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb
Requires:       dejavu-sans-mono-fonts

%description tests
Original release sources and notices plus mandatory private X11 child lifecycle,
focus, tab ordering, command argument and PTY foreground/background fixtures.
Upstream declares no test or check target.

%prep
%autosetup -p1
sed -n '1,4p' arg.h > LICENSE.arg
cat > downstream-qa.py <<'TABBED_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
"""Offline private-Xvfb and PTY fixtures, not native display/timing proof."""
import ctypes as C
import ctypes.util
import gzip
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import subprocess as S
import sys
import tarfile
import tempfile
import time

lib=C.CDLL(ctypes.util.find_library('X11'));D=C.c_void_p;U=C.c_ulong;I=C.c_int;L=C.c_long
def api(name,args,ret):
    f=getattr(lib,name);f.argtypes=args;f.restype=ret;return f
open_=api('XOpenDisplay',[C.c_char_p],D);close=api('XCloseDisplay',[D],I);rootwin=api('XDefaultRootWindow',[D],U)
atom=api('XInternAtom',[D,C.c_char_p,I],U);sync=api('XSync',[D,I],I);free=api('XFree',[D],I)
create=api('XCreateSimpleWindow',[D,U,I,I,C.c_uint,C.c_uint,C.c_uint,U,U],U)
destroy=api('XDestroyWindow',[D,U],I);map_=api('XMapWindow',[D,U],I);store=api('XStoreName',[D,U,C.c_char_p],I)
protocols=api('XSetWMProtocols',[D,U,C.POINTER(U),I],I);keycode=api('XKeysymToKeycode',[D,U],C.c_ubyte)
getfocus=api('XGetInputFocus',[D,C.POINTER(U),C.POINTER(I)],I)
tree=api('XQueryTree',[D,U,C.POINTER(U),C.POINTER(U),C.POINTER(C.POINTER(U)),C.POINTER(C.c_uint)],I)
geometry=api('XGetGeometry',[D,U,C.POINTER(U),C.POINTER(I),C.POINTER(I),C.POINTER(C.c_uint),C.POINTER(C.c_uint),C.POINTER(C.c_uint),C.POINTER(C.c_uint)],I)
get=api('XGetWindowProperty',[D,U,U,L,L,I,U,C.POINTER(U),C.POINTER(I),C.POINTER(U),C.POINTER(U),C.POINTER(D)],I)
set_=api('XChangeProperty',[D,U,U,U,I,I,D,I],I)
class Data(C.Union):_fields_=[('b',C.c_char*20),('s',C.c_short*10),('l',L*5)]
class Message(C.Structure):_fields_=[('type',I),('serial',U),('send_event',I),('display',D),('window',U),('message_type',U),('format',I),('data',Data)]
class Key(C.Structure):_fields_=[('type',I),('serial',U),('send_event',I),('display',D),('window',U),('root',U),('subwindow',U),('time',U),('x',I),('y',I),('x_root',I),('y_root',I),('state',C.c_uint),('keycode',C.c_uint),('same_screen',I)]
class Event(C.Union):_fields_=[('pad',L*24),('message',Message),('key',Key)]
send=api('XSendEvent',[D,U,I,L,C.POINTER(Event)],I);checkevent=api('XCheckTypedWindowEvent',[D,U,I,C.POINTER(Event)],I)
def until(check):
    end=time.monotonic()+15
    while time.monotonic()<end:
        value=check()
        if value:return value
        time.sleep(0.01)
    raise AssertionError('fixture condition timed out')
def write_report(path,data):
    temp=Path(str(path)+'.tmp');temp.write_text(json.dumps(data));temp.replace(path)
def is_delete(event,dpy,window,wmprotocols,wmdelete):
    message=event.message;assert message.window==window and message.format==32
    if message.message_type==wmprotocols:
        assert message.data.l[0]==wmdelete
        return True
    assert message.message_type==atom(dpy,b'_XEMBED',0)
    assert message.data.l[0]==0 and message.data.l[1]in(1,4)and list(message.data.l)[2:]==[0,0,0]
    return False
def client(report,xid):
    dpy=open_(None);assert dpy;parent=int(xid,0);w=create(dpy,parent,0,0,160,100,0,0,0)
    wmdelete=U(atom(dpy,b'WM_DELETE_WINDOW',0));wmprotocols=atom(dpy,b'WM_PROTOCOLS',0)
    protocols(dpy,w,C.byref(wmdelete),1);store(dpy,w,b'spawned-client');map_(dpy,w);sync(dpy,0)
    write_report(report,dict(window=w,parent=parent,xembed=os.environ.get('XEMBED'),argv=sys.argv[1:],pid=os.getpid()))
    def deleted():
        e=Event()
        if checkevent(dpy,w,33,C.byref(e)):
            return is_delete(e,dpy,w,wmprotocols,wmdelete.value)
    until(deleted);destroy(dpy,w);sync(dpy,0);close(dpy);Path(str(report)+'.done').write_text('WM_DELETE clean exit\n')
if sys.argv[1:2]==['--client']:
    assert len(sys.argv)==4;client(Path(sys.argv[2]),sys.argv[3]);sys.exit(0)

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/tabbed';xembed=root/'usr/bin/xembed';checks=[]
archive=root/'usr/share/tabbed/qa/tabbed-0.9.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='0acf87457b7419e66fbfa3a9cec95ffb46d254c6b88b5e4bb7cc18c3a92008a8'
with tarfile.open(archive,'r:gz')as tf:original={m.name:tf.extractfile(m).read()for m in tf.getmembers()if m.isfile()}
assert len(original)==9;lic=original['tabbed-0.9/LICENSE'];notice=original['tabbed-0.9/arg.h'].split(b'*/',1)[0]+b'*/\n'
for name in ('tabbed','tabbed-tests'):
    assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==lic
    assert(root/'usr/share/licenses'/name/'LICENSE.arg').read_bytes()==notice
assert(root/'usr/share/doc/tabbed/README').read_bytes()==original['tabbed-0.9/README']
for name in ('tabbed','xembed'):
    man=root/'usr/share/man/man1'/(name+'.1');data=man.read_bytes()if man.exists()else gzip.decompress(Path(str(man)+'.gz').read_bytes())
    assert data==original['tabbed-0.9/'+name+'.1'].replace(b'VERSION',b'0.9')
checks.append('original-nine-members-two-manpages-MIT-and-arg-notice')
env=dict(os.environ,LC_ALL='C');env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None);env.pop('XEMBED',None)
def run(program,args,code=0,environ=None):
    p=S.run([str(program),*args],env=env if environ is None else environ,stdout=S.PIPE,stderr=S.PIPE,timeout=15,start_new_session=True)
    assert p.returncode==code,(args,p.returncode,p.stdout,p.stderr);return p
p=run(binary,['-v'],1);assert not p.stdout and p.stderr=='tabbed-0.9, © 2009-2016 tabbed engineers, see LICENSE for details.\n'.encode()
for args in (['-?'],['-g'],['-n'],['-r'],['-p'],['-o'],['-O'],['-t'],['-T'],['-u'],['-U']):
    p=run(binary,args,1);assert not p.stdout and p.stderr.startswith(b'usage: ')and b'[-dfksv]'in p.stderr
p=run(binary,[],1);assert not p.stdout and p.stderr.endswith(b': cannot open display\n')
checks.append('original-cli-version-eleven-errors-and-no-display')
p=run(xembed,[],2);assert not p.stdout and p.stderr.startswith(b'usage: ')and p.stderr.endswith(b' flag cmd ...\n')
with tempfile.TemporaryDirectory(prefix='tabbed-qa-')as td:
    td=Path(td);fixture=td/'argv.py';fixture.write_text('#!/usr/bin/python3\nimport json,os,sys\nprint(json.dumps(dict(argv=sys.argv[1:],xembed=os.environ.get("XEMBED"))))\n');fixture.chmod(0o755)
    p=run(xembed,['--embed',str(fixture),'tail']);assert not p.stderr and json.loads(p.stdout)==dict(argv=['tail'],xembed=None)
    marked=dict(env,XEMBED='0x1234')
    p=run(xembed,['--embed',str(fixture),'tail'],environ=marked);assert not p.stderr and json.loads(p.stdout)==dict(argv=['tail'],xembed='0x1234')
    checks.append('xembed-usage-no-environment-and-no-controlling-tty')
    driver='''import fcntl,json,os,pty,signal,subprocess,sys,termios
signal.signal(signal.SIGHUP,signal.SIG_IGN)
os.setsid()
master,slave=pty.openpty()
fcntl.ioctl(slave,termios.TIOCSCTTY,0)
os.tcsetpgrp(slave,os.getpgrp())
p=subprocess.run(sys.argv[2:],stdin=slave,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setpgrp if sys.argv[1]=="background" else None,timeout=15)
assert p.returncode==0 and not p.stderr,(p.returncode,p.stdout,p.stderr)
sys.stdout.buffer.write(p.stdout)
os.close(slave);os.close(master)
'''
    for mode,expected in [('foreground',['--embed','0x1234','tail']),('background',['tail'])]:
        p=S.run([sys.executable,'-I','-B','-c',driver,mode,str(xembed),'--embed',str(fixture),'tail'],env=marked,stdout=S.PIPE,stderr=S.PIPE,timeout=20)
        assert p.returncode==0 and not p.stderr and json.loads(p.stdout)==dict(argv=expected,xembed='0x1234'),(mode,p.returncode,p.stdout,p.stderr)
    checks.append('xembed-private-pty-foreground-and-background')
    p=run(xembed,['--embed',str(td/'missing')],1);assert not p.stdout and b'No such file or directory'in p.stderr
    checks.append('xembed-exec-error-is-failure')
    rd,wr=os.pipe();server=None;dpy=None;processes=[]
    try:
        with open(td/'xvfb.stderr','wb')as log:
            try:server=S.Popen(['Xvfb','-displayfd',str(wr),'-screen','0','1024x768x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=S.DEVNULL,stderr=log)
            finally:os.close(wr)
            assert select.select([rd],[],[],15)[0],'Xvfb readiness missing';number=os.read(rd,64).strip();assert number.isdigit();env['DISPLAY']=':'+number.decode()
            dpy=open_(env['DISPLAY'].encode());assert dpy;rootwindow=rootwin(dpy)
            wmdelete=U(atom(dpy,b'WM_DELETE_WINDOW',0));wmprotocols=atom(dpy,b'WM_PROTOCOLS',0);selecttab=atom(dpy,b'_TABBED_SELECT_TAB',0);netname=atom(dpy,b'_NET_WM_NAME',0)
            def children(w):
                realroot=U();parent=U();out=C.POINTER(U)();n=C.c_uint();assert tree(dpy,w,C.byref(realroot),C.byref(parent),C.byref(out),C.byref(n))
                try:return parent.value,list(out[:n.value])
                finally:
                    if out:free(C.cast(out,D))
            def title(w):
                real=U();fmt=I();n=U();extra=U();data=D();assert get(dpy,w,netname,0,4096,0,0,C.byref(real),C.byref(fmt),C.byref(n),C.byref(extra),C.byref(data))==0
                try:return C.string_at(data,n.value)if data.value and fmt.value==8 else b''
                finally:
                    if data.value:free(data)
            def key(w,sym,state=4):
                e=Event();e.key.type=2;e.key.display=dpy;e.key.window=w;e.key.root=rootwindow;e.key.state=state;e.key.keycode=keycode(dpy,sym);e.key.same_screen=1
                assert send(dpy,w,0,1,C.byref(e));sync(dpy,0)
            def selected(w,expected):
                def ok():
                    focused=U();revert=I();getfocus(dpy,C.byref(focused),C.byref(revert));sync(dpy,0)
                    return focused.value==expected and title(w)==names[expected]
                until(ok)
            def delete_message(w):
                e=Event();e.message.type=33;e.message.display=dpy;e.message.window=w;e.message.message_type=wmprotocols;e.message.format=32;e.message.data.l[0]=wmdelete.value
                assert send(dpy,w,0,0,C.byref(e));sync(dpy,0)
            def start(args):
                p=S.Popen([str(binary),*args],env=env,stdout=S.PIPE,stderr=S.PIPE);processes.append(p)
                assert select.select([p.stdout],[],[],15)[0],'tabbed readiness missing';line=p.stdout.readline();assert line.startswith(b'0x')and line.endswith(b'\n');return p,int(line,16)
            def finish(p):
                out,err=p.communicate(timeout=15);assert p.returncode==0 and out==b''and err==b'',(p.returncode,out,err)
            def add(w,name):
                c=create(dpy,w,0,0,160,100,0,0,0);names[c]=name;protocols(dpy,c,C.byref(wmdelete),1);store(dpy,c,name);map_(dpy,c);sync(dpy,0);until(lambda:children(c)[0]==w);selected(w,c);return c
            names={};p,w=start(['-s','-c','-n','tabbed-fixture','-g','640x480']);one=add(w,b'one');two=add(w,b'two');three=add(w,b'three')
            assert set(children(w)[1])=={one,two,three}
            rr=U();x=I();y=I();width=C.c_uint();height=C.c_uint();border=C.c_uint();depth=C.c_uint()
            assert geometry(dpy,three,C.byref(rr),C.byref(x),C.byref(y),C.byref(width),C.byref(height),C.byref(border),C.byref(depth))and width.value==640 and y.value>0 and height.value+y.value==480 and border.value==0
            checks.append('three-child-parenting-focus-title-and-geometry')
            key(w,ord('l'),5);selected(w,two);key(w,ord('j'),5);key(w,ord('1'));selected(w,two);key(w,ord('2'));selected(w,three);key(w,0xff09);selected(w,two)
            raw=hex(one).encode();buf=C.create_string_buffer(raw);set_(dpy,w,selecttab,31,8,0,C.cast(buf,D),len(raw));sync(dpy,0);selected(w,one)
            checks.append('rotation-reorder-numeric-last-focus-and-property-selection')
            key(w,ord('q'))
            def hasdelete():
                e=Event()
                if checkevent(dpy,one,33,C.byref(e)):
                    return is_delete(e,dpy,one,wmprotocols,wmdelete.value)
            until(hasdelete);destroy(dpy,one);sync(dpy,0);until(lambda:one not in children(w)[1]);destroy(dpy,two);sync(dpy,0);until(lambda:two not in children(w)[1]);destroy(dpy,three);sync(dpy,0);finish(p)
            checks.append('ctrl-q-WM_DELETE-and-close-last-client-clean-exit')
            p,w=start(['-s','-n','delete-fixture']);names={};child=add(w,b'delete-child');delete_message(w);finish(p);assert children(child)[0]==rootwindow;destroy(dpy,child);sync(dpy,0)
            checks.append('container-WM_DELETE-reparents-client-and-exits-cleanly')
            for replace in (False,True):
                report=td/('spawn-replace.json'if replace else'spawn-append.json');command=[sys.executable,'-I','-B',str(Path(__file__).resolve()),'--client',str(report)]
                args=['-c','-n','spawn-fixture','-g','640x480']
                if replace:args+=['-r','6'];command+=['placeholder']
                p,w=start([*args,*command]);until(report.exists);data=json.loads(report.read_text());child=data['window'];assert data['parent']==w and int(data['xembed'],0)==w and data['argv']==['--client',str(report),str(w)]
                until(lambda:children(child)[0]==w and title(w)==b'spawned-client');key(w,ord('q'));until(Path(str(report)+'.done').exists);finish(p)
            checks.append('default-spawn-and-r-argument-replacement-XEMBED-child-lifecycle')
    finally:
        if dpy:close(dpy)
        os.close(rd)
        for p in processes:
            if p.poll()is None:p.terminate()
            try:p.wait(timeout=5)
            except S.TimeoutExpired:p.kill();p.wait(timeout=5)
        if server:
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('TABBED_QA_OK '+str(len(checks))+' '+','.join(checks))
TABBED_QA

%build
# Preserve original all target (tabbed and xembed), CPPFLAGS and linked libraries.
%make_build CC=gcc PREFIX=%{_prefix} CFLAGS='%{optflags}' LDFLAGS="%{?build_ldflags}"

%install
# Original install: all installs both executables, README and both man1 pages.
%make_install CC=gcc PREFIX=%{_prefix} DOCPREFIX=%{_docdir}/%{name} CFLAGS='%{optflags}' LDFLAGS="%{?build_ldflags}"
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE.arg %{buildroot}%{_licensedir}/%{name}/LICENSE.arg
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 LICENSE.arg %{buildroot}%{_licensedir}/%{name}-tests/LICENSE.arg
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# Original Makefile has no test/check target; no upstream test is skipped.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/LICENSE.arg
%doc %{_docdir}/%{name}/README
%{_bindir}/tabbed
%{_bindir}/xembed
%{_mandir}/man1/tabbed.1*
%{_mandir}/man1/xembed.1*

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%license %{_licensedir}/%{name}-tests/LICENSE.arg
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Tue Oct 20 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.9-1
- Preserve both default binaries and require offline private Xvfb and PTY QA.
