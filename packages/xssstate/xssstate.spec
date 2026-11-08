# SPDX-License-Identifier: Apache-2.0
Name:           xssstate
Version:        1.1
Release:        1
Summary:        Query the X11 screensaver extension state
License:        MIT
URL:            https://tools.suckless.org/x/xssstate/
Source0:        https://dl.suckless.org/tools/xssstate-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  libX11-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  python3


%description
Report the X11 screensaver state, idle milliseconds, or activation countdown.

%package tests
Summary:        Offline downstream screensaver protocol checks
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb

%description tests
Original source archive and bounded downstream Xvfb checks. These tests do not
provide physical-display, hardware, native timing, or screen-lock guarantees.

%prep
%autosetup -n xssstate-%{version}
cat > downstream-qa.py <<'XSSSTATE_QA'
# SPDX-License-Identifier: Apache-2.0
"""Bounded downstream Xvfb checks, not physical-display or timing evidence."""
import ctypes as C
import os
import pathlib
import re
import select
import subprocess as S
import sys
import tempfile

root=sys.argv[1]
tool=root+'/usr/bin/xssstate'
assert not sys.flags.optimize
base={'PATH':'/usr/bin:/bin','LC_ALL':'C','DISPLAY':':65530'}
def run(args,env,status=0):
 p=S.run([tool,*args],env=env,capture_output=True,timeout=10)
 assert p.returncode==status,(args,p.returncode,p.stdout,p.stderr)
 return p
for args,needle in [([],b'usage:'),(['-z'],b'usage:'),(['-v'],b'xssstate-1.1'),(['-s'],b'Cannot open display.')]:
 p=run(args,base,1);assert not p.stdout and needle in p.stderr
print('PASS xssstate usage, version exit and invalid display')
with tempfile.TemporaryDirectory(prefix='xssstate-qa-') as tmp:
 r,w=os.pipe();server=None;dpy=None
 try:
  with open(pathlib.Path(tmp)/'xvfb.log','wb') as log:
   server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(w),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],stdout=log,stderr=log,pass_fds=(w,),env=base)
   os.close(w);w=-1
   assert select.select([r],[],[],15)[0],'Xvfb startup timeout'
   number=os.read(r,32).strip();assert number.isdigit() and server.poll() is None
   env=dict(base,DISPLAY=':'+number.decode())
   x=C.CDLL('libX11.so.6');x.XOpenDisplay.argtypes=[C.c_char_p];x.XOpenDisplay.restype=C.c_void_p
   x.XCloseDisplay.argtypes=[C.c_void_p]
   x.XSetScreenSaver.argtypes=[C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_int]
   x.XForceScreenSaver.argtypes=[C.c_void_p,C.c_int]
   x.XSync.argtypes=[C.c_void_p,C.c_int]
   dpy=x.XOpenDisplay(env['DISPLAY'].encode());assert dpy
   x.XSetScreenSaver(dpy,3600,3600,1,1);x.XForceScreenSaver(dpy,0);x.XSync(dpy,0)
   assert run(['-s'],env).stdout==b'off\n'
   for option in ('-i','-t'):
    p=run([option],env);assert not p.stderr and re.fullmatch(rb'[0-9]+\n',p.stdout)
   assert run(['-ist'],env).stdout==b'off\n'
   assert re.fullmatch(rb'[0-9]+\n',run(['-it'],env).stdout)
   print('PASS xssstate off state, idle/countdown numeric and flag precedence')
   x.XForceScreenSaver(dpy,1);x.XSync(dpy,0)
   assert run(['-s'],env).stdout==b'on\n' and run(['-t'],env).stdout==b'0\n'
   print('PASS xssstate forced active state and zero countdown')
   x.XForceScreenSaver(dpy,0);x.XSync(dpy,0)
   assert run(['-s'],env).stdout==b'off\n'
   print('PASS xssstate reset returns off')
 finally:
  if dpy:x.XCloseDisplay(dpy)
  if w>=0:os.close(w)
  os.close(r)
  if server:
   server.terminate()
   try:server.wait(timeout=5)
   except S.TimeoutExpired:server.kill();server.wait(timeout=5)
XSSSTATE_QA

%build
%make_build CC=gcc CFLAGS="%{optflags} -std=c99 -pedantic -Wall -I. -DVERSION=\\\"%{version}\\\"" LDFLAGS="%{?build_ldflags} -L%{_libdir} -lc -lX11 -lXss"

%install
make install PREFIX=%{_prefix} MANPREFIX=%{_mandir} DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/xssstate/qa %{buildroot}%{_libexecdir}/xssstate-tests
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/xssstate/qa/xssstate-%{version}.tar.gz
install -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/xssstate-tests/qa.py

%check
python3 -I -B downstream-qa.py '%{buildroot}'

%files
%license LICENSE
%doc README xsidle.sh
%{_bindir}/xssstate
%{_mandir}/man1/xssstate.1*

%files tests
%license LICENSE
%{_datadir}/xssstate/
%{_libexecdir}/xssstate-tests/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1-1
- Preserve the official default build and add isolated Xvfb protocol checks.
