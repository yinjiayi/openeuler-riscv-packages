# SPDX-License-Identifier: Apache-2.0
Name:           dmenu
Version:        5.4
Release:        1%{?dist}
Summary:        Dynamic X11 menu and file filtering tools
License:        MIT
URL:            https://tools.suckless.org/dmenu/
Source0:        dmenu-5.4.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  python3
BuildRequires:  pkgconfig
BuildRequires:  libX11-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXft-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  dejavu-sans-mono-fonts
BuildRequires:  xorg-x11-server-Xvfb


%description
Unmodified suckless dmenu dynamic X11 menu, stest file-selection helper,
and the original dmenu_path and dmenu_run shell launchers.

%package tests
Summary:        Offline dmenu functional checks
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb
Requires:       dejavu-sans-mono-fonts

%description tests
Original fixed upstream source archive and downstream bounded offline
file-filter, cache and Xvfb keyboard-selection checks. These are not an
upstream test suite or evidence of native display or security behavior.

%prep
%autosetup -p1
cat > downstream-qa.py <<'DMENU_QA'
"""Downstream offline checks; upstream 5.4 has no test target."""
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

root = Path(sys.argv[1]).resolve()
bindir = root / 'usr/bin'
environment = dict(os.environ, LC_ALL='C', DISPLAY='', PATH=str(bindir)+':/usr/bin:/bin')
checks = []
def run(name, argv, expected=0, output=None, data=b'', env=None, cwd=None):
    q = S.run([str(x) for x in argv], input=data, stdout=S.PIPE, stderr=S.PIPE,
              timeout=15, env=environment if env is None else env, cwd=cwd)
    assert q.returncode == expected, (name, q.returncode, q.stdout, q.stderr)
    if output is not None:
        assert q.stdout == output, (name, q.stdout, output, q.stderr)
    checks.append(name)
    return q

archive = root / 'usr/share/dmenu/qa/dmenu-5.4.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == '8fbace2a0847aa80fe861066b118252dcc7b4ca0a0a8f3a93af02da8fb6cd453'
with tarfile.open(archive, 'r:gz') as upstream:
    for name in ('dmenu_path', 'dmenu_run'):
        assert (bindir/name).read_bytes() == upstream.extractfile('dmenu-5.4/'+name).read()
        run(name+'-shell-syntax', ['/bin/sh', '-n', bindir/name], output=b'')
    assert b'Permission is hereby granted' in upstream.extractfile('dmenu-5.4/LICENSE').read()
checks.append('original-archive-and-unpatched-scripts')
run('version', [bindir/'dmenu', '-v'], output=b'dmenu-5.4\n')
assert b'usage:' in run('invalid-option', [bindir/'dmenu', '-invalid'], 1, b'').stderr
assert b'cannot open display' in run('missing-display', [bindir/'dmenu'], 1, b'').stderr
assert b'usage:' in run('stest-invalid-option', [bindir/'stest', '-z'], 2, b'').stderr

with tempfile.TemporaryDirectory(prefix='dmenu-qa-') as temporary:
    work = Path(temporary)
    (work/'file').write_text('content\n')
    (work/'.hidden').write_text('hidden\n')
    (work/'program').write_text('#!/bin/sh\nexit 0\n')
    (work/'program').chmod(0o755)
    (work/'directory').mkdir()
    (work/'link').symlink_to('file')
    os.mkfifo(work/'pipe', 0o600)
    for option, name in (('-f','file'),('-d','directory'),('-h','link'),('-p','pipe'),('-x','program')):
        run('stest-'+option, [bindir/'stest',option,name], output=(name+'\n').encode(), cwd=work)
    run('stest-missing', [bindir/'stest','-e','absent'], 1, b'', cwd=work)
    run('stest-inverted', [bindir/'stest','-ve','absent'], output=b'absent\n', cwd=work)
    run('stest-hidden-default', [bindir/'stest','-f','.hidden'], 1, b'', cwd=work)
    run('stest-hidden-explicit', [bindir/'stest','-af','.hidden'], output=b'.hidden\n', cwd=work)
    run('stest-quiet', [bindir/'stest','-qf','file'], output=b'', cwd=work)
    run('stest-stdin', [bindir/'stest','-f'], output=b'file\nprogram\n', data=b'file\nabsent\nprogram\n', cwd=work)
    q=run('stest-directory-list', [bindir/'stest','-lfx',work])
    assert q.stdout == b'program\n'
    os.utime(work/'file',(1000000000,1000000000));os.utime(work/'program',(1000000010,1000000010))
    run('stest-newer', [bindir/'stest','-n','file','program'], output=b'program\n', cwd=work)
    run('stest-older', [bindir/'stest','-o','program','file'], output=b'file\n', cwd=work)
    cache_env=dict(environment,HOME=str(work),XDG_CACHE_HOME=str(work/'cache'),PATH=str(work)+':'+environment['PATH'])
    first=run('path-cache-create',[bindir/'dmenu_path'],env=cache_env).stdout
    assert b'program\n' in first and (work/'cache/dmenu_run').read_bytes()==first
    run('path-cache-reuse',[bindir/'dmenu_path'],output=first,env=cache_env)

    class Key(C.Structure):
        _fields_=[('type',C.c_int),('serial',C.c_ulong),('send_event',C.c_int),('display',C.c_void_p),
                  ('window',C.c_ulong),('root',C.c_ulong),('subwindow',C.c_ulong),('time',C.c_ulong),
                  ('x',C.c_int),('y',C.c_int),('x_root',C.c_int),('y_root',C.c_int),
                  ('state',C.c_uint),('keycode',C.c_uint),('same_screen',C.c_int)]
    class Event(C.Union):
        _fields_=[('key',Key),('pad',C.c_long*24)]
    x=C.CDLL(ctypes.util.find_library('X11'))
    def prototype(name, result, *args):
        f=getattr(x,name);f.restype=result;f.argtypes=list(args);return f
    op=prototype('XOpenDisplay',C.c_void_p,C.c_char_p)
    close=prototype('XCloseDisplay',C.c_int,C.c_void_p)
    defaultroot=prototype('XDefaultRootWindow',C.c_ulong,C.c_void_p)
    query=prototype('XQueryTree',C.c_int,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_ulong),C.POINTER(C.POINTER(C.c_ulong)),C.POINTER(C.c_uint))
    free=prototype('XFree',C.c_int,C.c_void_p)
    keycode=prototype('XKeysymToKeycode',C.c_ubyte,C.c_void_p,C.c_ulong)
    send=prototype('XSendEvent',C.c_int,C.c_void_p,C.c_ulong,C.c_int,C.c_long,C.POINTER(Event))
    flush=prototype('XFlush',C.c_int,C.c_void_p)
    rfd,wfd=os.pipe()
    with (work/'xvfb.log').open('wb') as log:
        server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wfd),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wfd,),stdout=log,stderr=log,env=environment)
        os.close(wfd);dpy=None
        try:
            assert select.select([rfd],[],[],15)[0], 'Xvfb display allocation timeout'
            number=os.read(rfd,64).strip();assert number.isdigit(),number
            display=b':'+number;dpy=op(display);assert dpy, 'cannot connect to private Xvfb'
            rootwin=defaultroot(dpy)
            def children():
                rt=C.c_ulong();parent=C.c_ulong();p=C.POINTER(C.c_ulong)();n=C.c_uint()
                assert query(dpy,rootwin,C.byref(rt),C.byref(parent),C.byref(p),C.byref(n))
                try:return {p[i] for i in range(n.value)}
                finally:
                    if p:free(p)
            for name, options, keys, expected, status in (
                ('select-default',[],[(0xff0d,0)],b'alpha\n',0),
                ('select-next',['-l','2','-b','-p','QA'],[(0xff54,0),(0xff0d,0)],b'beta\n',0),
                ('prefix-filter',[],[(ord('b'),0),(0xff0d,0)],b'beta\n',0),
                ('case-insensitive',['-i'],[(ord('b'),1),(0xff0d,0)],b'beta\n',0),
                ('literal-input',[],[(ord('z'),0),(0xff0d,1)],b'z\n',0),
                ('cancel',[],[(0xff1b,0)],b'',1)):
                before=children();p=S.Popen([str(bindir/'dmenu'),*options],stdin=S.PIPE,stdout=S.PIPE,stderr=S.PIPE,env=dict(environment,DISPLAY=display.decode()))
                try:
                    p.stdin.write(b'alpha\nbeta\nalphabet\n');p.stdin.close();p.stdin=None
                    deadline=time.monotonic()+15
                    while True:
                        windows=children()-before
                        if windows:break
                        assert p.poll() is None, (name,'early exit',p.communicate(timeout=1))
                        assert time.monotonic()<deadline, (name,'window timeout')
                        time.sleep(0.01)
                    assert len(windows)==1,(name,windows)
                    win=windows.pop()
                    for symbol,state in keys:
                        event=Event();event.key=Key(type=2,display=dpy,window=win,root=rootwin,state=state,keycode=keycode(dpy,symbol),same_screen=1)
                        assert event.key.keycode and send(dpy,win,0,1,C.byref(event))
                    flush(dpy)
                    stdout,stderr=p.communicate(timeout=15)
                    assert (p.returncode,stdout)==(status,expected),(name,p.returncode,stdout,stderr)
                    checks.append('xvfb-'+name)
                finally:
                    if p.poll() is None:p.kill();p.communicate(timeout=5)
        finally:
            if dpy:close(dpy)
            os.close(rfd)
            if server.poll() is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('DMENU_QA_OK '+str(len(checks))+' '+','.join(checks))
DMENU_QA

%build
# Retain upstream INCS, CPPFLAGS and LIBS, including VERSION and Xinerama.
%make_build CC=gcc X11INC=%{_includedir} X11LIB=%{_libdir} CFLAGS='%{optflags} -std=c99 -pedantic -Wall $(INCS) $(CPPFLAGS)' LDFLAGS='%{?build_ldflags} $(LIBS)'

%install
make install PREFIX=%{_prefix} MANPREFIX=%{_mandir} DESTDIR=%{buildroot}
install -d %{buildroot}%{_libexecdir}/dmenu-tests %{buildroot}%{_datadir}/dmenu/qa
install -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/dmenu-tests/qa.py
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/dmenu/qa/dmenu-5.4.tar.gz

%check
# Upstream has no test target. Keep its default all and run downstream checks.
python3 -I -B downstream-qa.py %{buildroot}

%files
%license LICENSE
%doc README
%{_bindir}/dmenu
%{_bindir}/stest
%{_bindir}/dmenu_path
%{_bindir}/dmenu_run
%{_mandir}/man1/dmenu.1*
%{_mandir}/man1/stest.1*

%files tests
%license LICENSE
%{_libexecdir}/dmenu-tests
%dir %{_datadir}/dmenu
%{_datadir}/dmenu/qa

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-1
- Package the original default build, scripts and MIT notices.
- Add bounded offline build and installed-package functional checks.
