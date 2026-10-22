# SPDX-License-Identifier: Apache-2.0
Name:           xdo
Version:        0.5.7
Release:        1%{?dist}
Summary:        Perform actions on X11 windows
License:        BSD-2-Clause
URL:            https://github.com/baskerville/xdo
Source0:        xdo-0.5.7.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  libX11

%description
Xdo performs actions on X11 windows using XCB. All upstream default
actions and the original manual are retained.

%package tests
Summary:        Offline Xvfb functional checks for xdo
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb
Requires:       libX11

%description tests
Downstream bounded checks against private Xvfb windows. These supplement
the upstream release, which has no test target; they do not test a native
display server, hardware, or security isolation.

%prep
%autosetup
cat > xdo-qa.py <<'XDO_QA'
"""Downstream bounded Xvfb checks for the unmodified upstream program."""
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

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/xdo'
env=dict(os.environ,LC_ALL='C',DISPLAY='')
checks=[]
def run(name,args,output=None,status=0):
    p=S.run([str(binary),*map(str,args)],env=env,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==status,(name,p.returncode,p.stdout,p.stderr)
    if output is not None:assert p.stdout==output,(name,p.stdout,output,p.stderr)
    checks.append(name);return p
archive=root/'usr/share/xdo/qa/xdo-0.5.7.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='b661229f0457939d3867cca1664c5671ae959b309feb58abe9142229c8c7ffb4'
with tarfile.open(archive,'r:gz')as original:
    assert original.getmember('xdo-0.5.7/README.asciidoc').linkname=='doc/xdo.1.txt'
    assert b'Redistribution and use' in original.extractfile('xdo-0.5.7/LICENSE').read()
run('version',['-v'],b'0.5.7\n')
run('usage',['-h'],b'xdo ACTION [OPTIONS] [WID ...]\n')
assert b'No arguments' in run('no-arguments',[],b'',1).stderr
assert b'Unknown action' in run('invalid-action',['unknown'],b'',1).stderr
assert b"Can't open display" in run('no-display',['id'],b'',1).stderr
x=C.CDLL(ctypes.util.find_library('X11'))
def proto(name,result,*args):
    f=getattr(x,name);f.restype=result;f.argtypes=list(args);return f
op=proto('XOpenDisplay',C.c_void_p,C.c_char_p);close=proto('XCloseDisplay',C.c_int,C.c_void_p)
defaultroot=proto('XDefaultRootWindow',C.c_ulong,C.c_void_p)
create=proto('XCreateSimpleWindow',C.c_ulong,C.c_void_p,C.c_ulong,C.c_int,C.c_int,C.c_uint,C.c_uint,C.c_uint,C.c_ulong,C.c_ulong)
mapwin=proto('XMapWindow',C.c_int,C.c_void_p,C.c_ulong)
destroy=proto('XDestroyWindow',C.c_int,C.c_void_p,C.c_ulong)
sync=proto('XSync',C.c_int,C.c_void_p,C.c_int)
atom=proto('XInternAtom',C.c_ulong,C.c_void_p,C.c_char_p,C.c_int)
property_=proto('XChangeProperty',C.c_int,C.c_void_p,C.c_ulong,C.c_ulong,C.c_ulong,C.c_int,C.c_int,C.c_void_p,C.c_int)
store=proto('XStoreName',C.c_int,C.c_void_p,C.c_ulong,C.c_char_p)
geometry=proto('XGetGeometry',C.c_int,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_int),C.POINTER(C.c_int),C.POINTER(C.c_uint),C.POINTER(C.c_uint),C.POINTER(C.c_uint),C.POINTER(C.c_uint))
query=proto('XQueryTree',C.c_int,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_ulong),C.POINTER(C.POINTER(C.c_ulong)),C.POINTER(C.c_uint))
free=proto('XFree',C.c_int,C.c_void_p)
class Attributes(C.Structure):
    _fields_=[('x',C.c_int),('y',C.c_int),('width',C.c_int),('height',C.c_int),('border_width',C.c_int),('depth',C.c_int),('visual',C.c_void_p),('root',C.c_ulong),('class_',C.c_int),('bit_gravity',C.c_int),('win_gravity',C.c_int),('backing_store',C.c_int),('backing_planes',C.c_ulong),('backing_pixel',C.c_ulong),('save_under',C.c_int),('colormap',C.c_ulong),('map_installed',C.c_int),('map_state',C.c_int),('all_event_masks',C.c_long),('your_event_mask',C.c_long),('do_not_propagate_mask',C.c_long),('override_redirect',C.c_int),('screen',C.c_void_p)]
attributes=proto('XGetWindowAttributes',C.c_int,C.c_void_p,C.c_ulong,C.POINTER(Attributes))
with tempfile.TemporaryDirectory(prefix='xdo-qa-')as temp:
    rd,wr=os.pipe()
    with (Path(temp)/'xvfb.log').open('wb')as log:
        server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=log,stderr=log,env=env)
        os.close(wr);dpy=None;windows=[]
        try:
            assert select.select([rd],[],[],15)[0],'Xvfb allocation timeout'
            number=os.read(rd,64).strip();assert number.isdigit()
            env['DISPLAY']=':'+number.decode();dpy=op(env['DISPLAY'].encode());assert dpy
            rootwin=defaultroot(dpy)
            for offset in (0,1):
                w=create(dpy,rootwin,10+offset,20,100,80,0,0,0);assert w;windows.append(w);mapwin(dpy,w)
            window,other=windows
            def set32(w,name,type_,value):
                datum=C.c_ulong(value);property_(dpy,w,atom(dpy,name,0),type_,32,0,C.byref(datum),1)
            set32(rootwin,b'_NET_ACTIVE_WINDOW',33,window)
            set32(window,b'_NET_WM_PID',6,os.getpid())
            store(dpy,window,b'xdo-qa-window')
            cls=C.create_string_buffer(b'xdo-qa-instance\0XdoQaClass\0')
            property_(dpy,window,atom(dpy,b'WM_CLASS',0),31,8,0,cls,len(cls.raw)-1)
            sync(dpy,0)
            wid='0x%%08X'%%window
            run('explicit-id',['id',wid],(wid+'\n').encode())
            run('active-id',['id'],(wid+'\n').encode())
            run('pid',['pid',wid],(str(os.getpid())+'\n').encode())
            for option,value in (('-a','xdo-qa-window'),('-n','xdo-qa-instance'),('-N','XdoQaClass'),('-p',str(os.getpid()))):
                run('match-'+option,['id',option,value],(wid+'\n').encode())
            run('no-match',['id','-N','NoSuchQaClass'],b'',1)
            def geom():
                rt=C.c_ulong();xx=C.c_int();yy=C.c_int();ww=C.c_uint();hh=C.c_uint();border=C.c_uint();depth=C.c_uint()
                assert geometry(dpy,window,C.byref(rt),C.byref(xx),C.byref(yy),C.byref(ww),C.byref(hh),C.byref(border),C.byref(depth))
                return xx.value,yy.value,ww.value,hh.value
            run('move-absolute',['move','-x','31','-y','42',wid],b'');assert geom()==(31,42,100,80)
            run('move-relative',['move','-x','+3','-y','-2',wid],b'');assert geom()==(34,40,100,80)
            run('resize-absolute',['resize','-w','120','-h','90',wid],b'');assert geom()==(34,40,120,90)
            run('resize-relative',['resize','-w','-5','-h','+7',wid],b'');assert geom()==(34,40,115,97)
            def stacking():
                rt=C.c_ulong();parent=C.c_ulong();items=C.POINTER(C.c_ulong)();count=C.c_uint()
                assert query(dpy,rootwin,C.byref(rt),C.byref(parent),C.byref(items),C.byref(count))
                try:return [items[i]for i in range(count.value)]
                finally:
                    if items:free(items)
            run('raise',['raise',wid],b'');assert stacking().index(window)>stacking().index(other)
            run('lower',['lower',wid],b'');assert stacking().index(window)<stacking().index(other)
            run('above',['above','-t',str(other),wid],b'');assert stacking().index(window)>stacking().index(other)
            run('below',['below','-t',str(other),wid],b'');assert stacking().index(window)<stacking().index(other)
            def mapped():
                a=Attributes();assert attributes(dpy,window,C.byref(a));return a.map_state
            assert mapped()==2
            run('hide',['hide',wid],b'');assert mapped()==0 and geom()==(34,40,115,97)
            run('show',['show',wid],b'');assert mapped()==2 and geom()==(34,40,115,97)
        finally:
            if dpy:
                for w in windows:destroy(dpy,w)
                close(dpy)
            os.close(rd)
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('XDO_QA_OK '+str(len(checks))+' '+','.join(checks))
XDO_QA

%build
# The fixed release VERSION is used, never the outer packaging Git checkout.
%make_build VERCMD='cat VERSION' CC=gcc CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Wextra' LDFLAGS='%{?build_ldflags}'

%install
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir}
install -D -m 0644 xdo-qa.py %{buildroot}%{_libexecdir}/xdo-tests/qa.py
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/xdo/qa/xdo-0.5.7.tar.gz

%check
/usr/bin/python3 -I -B xdo-qa.py %{buildroot}

%files
%license LICENSE
%doc doc/xdo.1.txt
%{_bindir}/xdo
%{_mandir}/man1/xdo.1*

%files tests
%license LICENSE
%dir %{_libexecdir}/xdo-tests
%{_libexecdir}/xdo-tests/qa.py
%dir %{_datadir}/xdo
%dir %{_datadir}/xdo/qa
%{_datadir}/xdo/qa/xdo-0.5.7.tar.gz

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.7-1
- Package the unmodified default build and manual with offline Xvfb checks.
