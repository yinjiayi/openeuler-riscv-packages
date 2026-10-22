# SPDX-License-Identifier: Apache-2.0
Name:           lsw
Version:        0.3
Release:        1
Summary:        List X11 window titles and identifiers
License:        MIT
URL:            https://tools.suckless.org/x/lsw/
Source0:        https://dl.suckless.org/tools/lsw-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  libX11-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  python3

%description
Print the XID and title of viewable, non-override-redirect X11 child windows.

%package tests
Summary:        Offline downstream Xvfb checks for lsw
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb

%description tests
Bounded isolated-Xvfb functional checks and the unchanged official source
archive. These are downstream checks, not an upstream suite or native graphics,
hardware, timing or performance validation.

%prep
%autosetup -n lsw-%{version}
cat > downstream-qa.py <<'LSW_QA'
# SPDX-License-Identifier: Apache-2.0
"""Downstream offline X11 functional checks; not hardware/display validation."""
import ctypes as c
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

root=Path(sys.argv[1] or '/')
tool=root/'usr/bin/lsw'
archive=root/'usr/share/lsw/qa/lsw-0.3.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='0b3f3ce16eef060df6e0d90327ee82593dfd75281347908698747cfa3f8d0655'
env=dict(os.environ,LC_ALL='C',DISPLAY=':65534')
bad=subprocess.run([str(tool)],env=env,capture_output=True,timeout=10)
assert bad.returncode!=0 and not bad.stdout and b'cannot open display' in bad.stderr
x=c.CDLL('libX11.so.6')
def declare(name,restype,*args):
    f=getattr(x,name);f.restype=restype;f.argtypes=list(args);return f
ptr=c.c_void_p;win=c.c_ulong;integer=c.c_int
open_display=declare('XOpenDisplay',ptr,c.c_char_p)
close_display=declare('XCloseDisplay',integer,ptr)
default_root=declare('XDefaultRootWindow',win,ptr)
create=declare('XCreateSimpleWindow',win,ptr,win,integer,integer,c.c_uint,c.c_uint,c.c_uint,c.c_ulong,c.c_ulong)
store=declare('XStoreName',integer,ptr,win,c.c_char_p)
atom=declare('XInternAtom',c.c_ulong,ptr,c.c_char_p,integer)
prop=declare('XChangeProperty',integer,ptr,win,c.c_ulong,c.c_ulong,integer,integer,c.c_char_p,integer)
mapping=declare('XMapWindow',integer,ptr,win)
sync=declare('XSync',integer,ptr,integer)
destroy=declare('XDestroyWindow',integer,ptr,win)
attrs=declare('XChangeWindowAttributes',integer,ptr,win,c.c_ulong,ptr)
class Attributes(c.Structure):
    _fields_=[('background_pixmap',c.c_ulong),('background_pixel',c.c_ulong),('border_pixmap',c.c_ulong),('border_pixel',c.c_ulong),('bit_gravity',integer),('win_gravity',integer),('backing_store',integer),('backing_planes',c.c_ulong),('backing_pixel',c.c_ulong),('save_under',integer),('event_mask',c.c_long),('do_not_propagate_mask',c.c_long),('override_redirect',integer),('colormap',c.c_ulong),('cursor',c.c_ulong)]
with tempfile.TemporaryDirectory(prefix='lsw-qa-') as work:
    work=Path(work)
    with (work/'server.log').open('wb') as log:
        # Allocate a server-selected unused display, not a fixed shared port.
        with (work/'display').open('w+b') as display:
            server=subprocess.Popen(['/usr/bin/Xvfb','-displayfd',str(display.fileno()),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(display.fileno(),),stdout=log,stderr=log)
            d=None
            try:
                for _ in range(100):
                    assert server.poll() is None,(work/'server.log').read_text()
                    display.seek(0);number=display.read().strip()
                    if number:
                        assert number.isdigit();env['DISPLAY']=':'+number.decode()
                        d=open_display(env['DISPLAY'].encode())
                        if d:break
                    time.sleep(0.1)
                assert d,'isolated Xvfb did not become ready'
                parent=default_root(d)
                def window(p,name,visible=True,override=False):
                    w=create(d,p,0,0,100,80,0,0,0);assert w
                    store(d,w,name.encode())
                    if override:
                        a=Attributes();a.override_redirect=1;attrs(d,w,1<<9,c.byref(a))
                    if visible:mapping(d,w)
                    return w
                first=window(parent,'fallback')
                hidden=window(parent,'hidden',False)
                ignored=window(parent,'override',override=True)
                nested=window(parent,'parent')
                child=window(nested,'child')
                value=b'modern-title'
                prop(d,first,atom(d,b'_NET_WM_NAME',0),atom(d,b'UTF8_STRING',0),8,0,value,len(value))
                sync(d,0)
                def run(*args):
                    p=subprocess.run([str(tool),*args],env=env,capture_output=True,timeout=10)
                    assert p.returncode==0 and not p.stderr,(p.returncode,p.stderr)
                    return p.stdout.decode().splitlines()
                fmt=lambda w,name:'0x{:07x} {}'.format(w,name)
                expected={fmt(first,'modern-title'),fmt(nested,'parent')}
                assert set(run())==expected
                assert set(run(hex(parent)))==expected
                assert run(hex(nested))==[fmt(child,'child')]
                assert set(run(hex(parent),hex(nested)))==expected|{fmt(child,'child')}
                mapping(d,hidden);sync(d,0)
                assert set(run())==expected|{fmt(hidden,'hidden')}
                destroy(d,hidden);sync(d,0)
                assert set(run())==expected
                print('PASS lsw offline Xvfb root/explicit/nested selection, visibility, override filtering, modern/fallback names and missing display')
            finally:
                if d:close_display(d)
                server.terminate()
                try:server.wait(timeout=5)
                except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
LSW_QA

%build
# Preserve default all and Xlib functionality; distro flags/paths only.
%make_build CC=gcc X11INC=%{_includedir} X11LIB=%{_libdir} CFLAGS="%{optflags} -ansi -pedantic -Wall -I%{_includedir}" LDFLAGS="%{?build_ldflags} -L%{_libdir} -lX11"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -Dpm0644 downstream-qa.py %{buildroot}%{_libexecdir}/lsw-tests/qa.py
install -Dpm0644 %{SOURCE0} %{buildroot}%{_datadir}/lsw/qa/lsw-%{version}.tar.gz

%check
# Upstream has no check/test target. Same checks run after ordinary DNF install.
python3 -I -B %{buildroot}%{_libexecdir}/lsw-tests/qa.py %{buildroot}

%files
%license LICENSE
%doc README
%{_bindir}/lsw
%{_mandir}/man1/lsw.1*

%files tests
%license LICENSE
%{_libexecdir}/lsw-tests/
%{_datadir}/lsw/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.3-1
- Preserve official default build and add offline Xvfb functional checks.
