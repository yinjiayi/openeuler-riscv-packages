# SPDX-License-Identifier: MIT
Name:           wmname
Version:        0.1
Release:        1%{?dist}
Summary:        Print or set the X11 EWMH window manager name
License:        MIT
URL:            https://tools.suckless.org/x/wmname/
Source0:        wmname-0.1.tar.gz
Patch0:         patches/0001-defer-stripping-to-rpm.patch
Patch1:         patches/0002-read-complete-typed-property.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3
BuildRequires:  libX11-devel
BuildRequires:  xorg-x11-server-Xvfb


%description
Print or set the EWMH window manager name on an X11 root window.

%package tests
Summary:        Offline private-Xvfb functional checks for wmname
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb

%description tests
Retained official source and notices plus downstream command and property
boundary checks. Upstream declares no test or check target.

%prep
%autosetup -p1
cat > downstream-qa.py <<'WMNAME_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
"""Private X11 checks; not native display, timing or security proof."""
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
root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/wmname';checks=[]
archive=root/'usr/share/wmname/qa/wmname-0.1.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='559ad188b2913167dcbb37ecfbb7ed474a7ec4bbcb0129d8d5d08cb9208d02c5'
with tarfile.open(archive,'r:gz')as tf:
    original={m.name:tf.extractfile(m).read()for m in tf.getmembers()if m.isfile()}
assert len(original)==5
lic=original['wmname-0.1/LICENSE'];assert b'MIT/X Consortium License'in lic and b'Permission is hereby granted'in lic
for name in ('wmname','wmname-tests'):assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==lic
assert(root/'usr/share/doc/wmname/README').read_bytes()==original['wmname-0.1/README']
checks.append('original-five-member-archive-and-notices')
env=dict(os.environ,LC_ALL='C');env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
def run(args,code=0):
    p=S.run([str(binary),*args],env=env,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==code,(args,p.returncode,p.stdout,p.stderr)
    return p
p=run(['-v'],1);assert not p.stdout and p.stderr=='wmname-0.1, © 2008 Anselm R Garbe\n'.encode()
checks.append('original-version-status-without-display')
p=run(['a','b'],1);assert not p.stdout and p.stderr==b'usage: wmname [name] [-v]\n'
checks.append('original-usage-without-display')
p=run([],1);assert not p.stdout and p.stderr==b'wmname: cannot open display\n'
checks.append('no-display-fails')
lib=C.CDLL(ctypes.util.find_library('X11'));D=C.c_void_p;U=C.c_ulong;I=C.c_int
def api(name,args,ret):
    f=getattr(lib,name);f.argtypes=args;f.restype=ret;return f
open_=api('XOpenDisplay',[C.c_char_p],D);close=api('XCloseDisplay',[D],I)
rootwin=api('XDefaultRootWindow',[D],U);atom=api('XInternAtom',[D,C.c_char_p,I],U)
sync=api('XSync',[D,I],I);free=api('XFree',[D],I)
get=api('XGetWindowProperty',[D,U,U,C.c_long,C.c_long,I,U,C.POINTER(U),C.POINTER(I),C.POINTER(U),C.POINTER(U),C.POINTER(D)],I)
set_=api('XChangeProperty',[D,U,U,U,I,I,D,I],I);delete=api('XDeleteProperty',[D,U,U],I)
with tempfile.TemporaryDirectory(prefix='wmname-qa-')as td:
    rd,wr=os.pipe();server=None;dpy=None
    try:
        with open(Path(td)/'xvfb.stderr','wb')as log:
            try:server=S.Popen(['Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=S.DEVNULL,stderr=log)
            finally:os.close(wr)
            assert select.select([rd],[],[],15)[0],'private Xvfb did not become ready'
            number=os.read(rd,64).strip();assert number.isdigit();env['DISPLAY']=':'+number.decode()
            dpy=open_(env['DISPLAY'].encode());assert dpy
            win=rootwin(dpy);nameatom=atom(dpy,b'_NET_WM_NAME',0);checkatom=atom(dpy,b'_NET_SUPPORTING_WM_CHECK',0);utf8=atom(dpy,b'UTF8_STRING',0)
            def read(prop):
                real=U();fmt=I();n=U();extra=U();data=D()
                assert get(dpy,win,prop,0,65536,0,0,C.byref(real),C.byref(fmt),C.byref(n),C.byref(extra),C.byref(data))==0 and extra.value==0
                try:
                    out=list(C.cast(data,C.POINTER(U))[:n.value])if fmt.value==32 else C.string_at(data,n.value)if data.value else b''
                    return real.value,fmt.value,out
                finally:
                    if data.value:free(data)
            delete(dpy,win,nameatom);sync(dpy,0);p=run([]);assert not p.stdout and not p.stderr
            checks.append('missing-property-is-empty-output')
            for value in ('','x','LG3D','a'*127,'b'*128,'c'*129,'d'*1024,'窗'*100,'z'*16384):
                p=run([value]);assert not p.stdout and not p.stderr
                assert read(nameatom)==(utf8,8,value.encode())and read(checkatom)==(33,32,[win])
                p=run([]);assert p.stdout==value.encode()+b'\n'and not p.stderr
            checks.append('nine-set-get-byte-boundaries-and-supporting-window')
            buf=C.create_string_buffer(b'wrong-type');set_(dpy,win,nameatom,31,8,0,C.cast(buf,D),len(buf.value));sync(dpy,0)
            p=run([],1);assert not p.stdout and p.stderr==b'wmname: cannot read complete UTF8_STRING property\n'
            checks.append('wrong-property-type-fails')
            word=U(42);set_(dpy,win,nameatom,utf8,32,0,C.cast(C.byref(word),D),1);sync(dpy,0)
            p=run([],1);assert not p.stdout and p.stderr==b'wmname: cannot read complete UTF8_STRING property\n'
            checks.append('wrong-property-format-fails')
    finally:
        if dpy:close(dpy)
        os.close(rd)
        if server:
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('WMNAME_QA_OK '+str(len(checks))+' '+','.join(checks))
WMNAME_QA

%build
# Retain original all/C99/pedantic/Wall/-Os/VERSION/Xlib; RPM owns stripping.
%make_build CC=gcc LD=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"

%install
%make_install CC=gcc LD=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 README %{buildroot}%{_docdir}/%{name}/README
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# Original Makefile declares no test/check target. No upstream test is skipped.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_bindir}/wmname

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Tue Oct 20 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.1-1
- Preserve default build and verify full typed-property boundaries offline.
