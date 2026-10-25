# SPDX-License-Identifier: MIT
Name:           swarp
Version:        0.1
Release:        1%{?dist}
Summary:        Simple X11 pointer warping utility
License:        MIT
URL:            https://tools.suckless.org/x/swarp/
Source0:        swarp-0.1.tar.gz
Patch0:         patches/0001-defer-stripping-to-rpm.patch
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
Move the X11 pointer to absolute screen coordinates and focus PointerRoot.
This is the suckless utility, not the unrelated astronomical image resampler.

%package tests
Summary:        Offline private-Xvfb functional checks for swarp
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb

%description tests
Retained original source and license plus downstream coordinate, focus and
command-interface checks. Upstream declares no test or check target.

%prep
%setup -q
%patch0 -p1
cat > downstream-qa.py <<'SWARP_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
"""Private Xvfb functional checks; not native input, timing or security proof."""
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

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/swarp';checks=[]
archive=root/'usr/share/swarp/qa/swarp-0.1.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ef5730fe8ee00879cbec1e91e22a7f0f7817a63375d790d775f5b7427886d45f'
with tarfile.open(archive,'r:gz')as tf:
    original={m.name:tf.extractfile(m).read()for m in tf.getmembers()if m.isfile()}
assert len(original)==5
license_=original['swarp-0.1/LICENSE']
assert b'Anselm R. Garbe'in license_ and b'Sander van Dijk'in license_ and b'Permission is hereby granted'in license_
for name in ('swarp','swarp-tests'):
    assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==license_
assert(root/'usr/share/doc/swarp/README').read_bytes()==original['swarp-0.1/README']
checks.append('original-five-member-archive-and-notices')
env=dict(os.environ,LC_ALL='C',DISPLAY='')
def run(args,status=0):
    p=S.run([str(binary),*args],env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=20)
    assert p.returncode==status,(args,p.returncode,p.stdout,p.stderr)
    return p
p=run(['-v']);assert p.stdout==b'swarp-0.1, (C)opyright MMVI Anselm R. Garbe\n'and not p.stderr
checks.append('version-without-display')
for args in ([],['1'],['1','2','3'],['--version']):
    p=run(args,1);assert not p.stdout and p.stderr==b'usage: swarp <x> <y> [-v]\n'
checks.append('original-argument-count-and-usage')
p=run(['1','2'],1);assert not p.stdout and p.stderr==b'swarp: cannot open display\n'
checks.append('no-display-fails')
x=C.CDLL(ctypes.util.find_library('X11'))
def proto(name,result,*args):
    f=getattr(x,name);f.restype=result;f.argtypes=list(args);return f
op=proto('XOpenDisplay',C.c_void_p,C.c_char_p)
close=proto('XCloseDisplay',C.c_int,C.c_void_p)
sync=proto('XSync',C.c_int,C.c_void_p,C.c_int)
rootwin=proto('XDefaultRootWindow',C.c_ulong,C.c_void_p)
query=proto('XQueryPointer',C.c_int,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_ulong),C.POINTER(C.c_int),C.POINTER(C.c_int),C.POINTER(C.c_int),C.POINTER(C.c_int),C.POINTER(C.c_uint))
setfocus=proto('XSetInputFocus',C.c_int,C.c_void_p,C.c_ulong,C.c_int,C.c_ulong)
getfocus=proto('XGetInputFocus',C.c_int,C.c_void_p,C.POINTER(C.c_ulong),C.POINTER(C.c_int))
with tempfile.TemporaryDirectory(prefix='swarp-qa-')as temporary:
    env['HOME']=temporary;env['XDG_CACHE_HOME']=temporary
    rd,wr=os.pipe();dpy=None;server=None
    try:
        with(Path(temporary)/'xvfb.log').open('wb')as log:
            try:server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=log,stderr=log,env=env)
            finally:os.close(wr)
            assert select.select([rd],[],[],20)[0],'private display allocation timeout'
            number=os.read(rd,64).strip();assert number.isdigit()
            env['DISPLAY']=':'+number.decode();dpy=op(env['DISPLAY'].encode());assert dpy
            window=rootwin(dpy)
            def position():
                rr=C.c_ulong();child=C.c_ulong();rx=C.c_int();ry=C.c_int();wx=C.c_int();wy=C.c_int();mask=C.c_uint()
                sync(dpy,0);assert query(dpy,window,C.byref(rr),C.byref(child),C.byref(rx),C.byref(ry),C.byref(wx),C.byref(wy),C.byref(mask))
                assert rr.value==window
                return rx.value,ry.value
            def focus():
                f=C.c_ulong();r=C.c_int();sync(dpy,0);getfocus(dpy,C.byref(f),C.byref(r));return f.value,r.value
            for args,expected in ((['17','19'],(17,19)),(['0','0'],(0,0)),(['639','479'],(639,479)),(['-5','-7'],(0,0)),(['700','600'],(639,479)),(['17tail','19trailing'],(17,19)),([' 7',' 11'],(7,11))):
                setfocus(dpy,window,2,0);sync(dpy,0)
                p=run(args);assert not p.stdout and not p.stderr
                assert position()==expected,(args,position(),expected)
                assert focus()==(1,1),focus()
            checks.append('seven-coordinate-and-PointerRoot-focus-cases')
            for args in (['bad','2'],['1','bad'],['','2']):
                before=position();setfocus(dpy,window,2,0);sync(dpy,0);oldfocus=focus()
                p=run(args,1);assert not p.stdout and p.stderr==b'usage: swarp <x> <y> [-v]\n'
                assert position()==before and focus()==oldfocus
            checks.append('invalid-coordinate-has-no-warp-or-focus-change')
    finally:
        if dpy:close(dpy)
        os.close(rd)
        if server:
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('SWARP_QA_OK '+str(len(checks))+' '+','.join(checks))
SWARP_QA

%build
# Preserve upstream -Os, VERSION define, default all target and Xlib linkage.
%make_build CC=gcc LD=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"

%install
%make_install CC=gcc LD=gcc X11INC=%{_includedir} X11LIB=%{_libdir} PREFIX=%{_prefix} CFLAGS='%{optflags} -Os -I. -I%{_includedir} -DVERSION=\"%{version}\"' LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11"
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 README %{buildroot}%{_docdir}/%{name}/README
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# The original Makefile has no test/check target. No upstream tests are skipped.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_bindir}/swarp

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.1-1
- Retain default X11 behavior and add offline staged/installed checks.
