# SPDX-License-Identifier: Apache-2.0
Name:           unclutter-xfixes
Version:        1.6
Release:        1%{?dist}
Summary:        Hide an idle X11 cursor using Xfixes
License:        MIT
URL:            https://github.com/Airblader/unclutter-xfixes
Source0:        unclutter-xfixes-1.6.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  pkgconfig
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libev-devel
BuildRequires:  asciidoc
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtds
BuildRequires:  python3
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  libXtst

%description
Unclutter-xfixes hides an idle X11 cursor using the Xfixes and XInput2
extensions. The unmodified default program, options and manual are retained.
Its command is named unclutter; this is the Xfixes rewrite, not the older
unrelated implementation of that command.

%package tests
Summary:        Offline Xvfb lifecycle checks for unclutter-xfixes
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       xorg-x11-server-Xvfb
Requires:       libX11
Requires:       libXtst

%description tests
Downstream bounded Xvfb/XTEST checks of CLI status, default idle handling
and XI2 hide/show lifecycle traces. These supplement an upstream release
without a test target. They are not cursor-pixel, physical input, touch,
native display, security isolation or performance validation.

%prep
%autosetup
cat > downstream-qa.py <<'UNCLUTTER_QA'
"""Offline Xvfb/XTEST lifecycle traces, not cursor-pixel or native-input proof."""
import ctypes as C
import ctypes.util
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

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/unclutter'
env=dict(os.environ,LC_ALL='C',DISPLAY='');checks=[]
archive=root/'usr/share/unclutter-xfixes/qa/unclutter-xfixes-1.6.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='6f7f248f16b7d4ec7cb144b6bc5a66bd49078130513a184f4dc16c498d457db9'
with tarfile.open(archive,'r:gz')as tf:
    license_=tf.extractfile('unclutter-xfixes-1.6/LICENSE').read()
    assert b'Ingo B' in license_ and b'Permission is hereby granted' in license_
    for name in ('unclutter-xfixes','unclutter-xfixes-tests'):
        assert (root/'usr/share/licenses'/name/'LICENSE').read_bytes()==license_
checks.append('fixed-original-archive-and-license')
def run(name,args,status,needle):
    p=S.run([str(binary),*args],env=env,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==status and not p.stdout and needle in p.stderr,(name,p.returncode,p.stdout,p.stderr)
    checks.append(name);return p
for flag in ('-v','--version'):
    assert run('version-'+flag,[flag],0,b'unclutter-xfixes version 1.6\n').stderr==b'unclutter-xfixes version 1.6\n'
run('help',['--help'],1,b'Usage:')
run('unknown-option',['--unknown-qa-option'],1,b'Usage:')
run('missing-display',[],1,b'Failed to connect to the X server.')
run('invalid-timeout',['--timeout','-1'],1,b'Invalid timeout specified.')
run('invalid-jitter',['--jitter','-1'],1,b'Invalid jitter value specified.')
run('invalid-button-list',['--ignore-buttons','invalid'],1,b'no button could be parsed')
x=C.CDLL(ctypes.util.find_library('X11'));xt=C.CDLL(ctypes.util.find_library('Xtst'))
def proto(lib,name,result,*args):
    f=getattr(lib,name);f.restype=result;f.argtypes=list(args);return f
op=proto(x,'XOpenDisplay',C.c_void_p,C.c_char_p)
close=proto(x,'XCloseDisplay',C.c_int,C.c_void_p)
sync=proto(x,'XSync',C.c_int,C.c_void_p,C.c_int)
motion=proto(xt,'XTestFakeMotionEvent',C.c_int,C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_ulong)
button=proto(xt,'XTestFakeButtonEvent',C.c_int,C.c_void_p,C.c_uint,C.c_int,C.c_ulong)
with tempfile.TemporaryDirectory(prefix='unclutter-qa-')as temporary:
    rd,wr=os.pipe()
    with (Path(temporary)/'xvfb.log').open('wb')as log:
        server=S.Popen(['/usr/bin/Xvfb','-displayfd',str(wr),'-screen','0','640x480x24','-nolisten','tcp','-noreset'],pass_fds=(wr,),stdout=log,stderr=log,env=env)
        os.close(wr);dpy=None
        try:
            assert select.select([rd],[],[],15)[0],'private display allocation timeout'
            number=os.read(rd,64).strip();assert number.isdigit()
            env['DISPLAY']=':'+number.decode();dpy=op(env['DISPLAY'].encode());assert dpy
            for case,(name,args,wakeup) in enumerate((
                ('original-default-idle',[], 'motion'),
                ('start-hidden-motion',['--start-hidden','--timeout','60'],'motion'),
                ('start-hidden-button',['--start-hidden','--timeout','60','--ignore-buttons','4,5'],'button'),
                ('legacy-idle',['--idle','0.2','--onescreen'],'motion'),
                ('explicit-display',['--display',env['DISPLAY'],'--start-hidden','--timeout','60'],'motion'))):
                master,slave=pty.openpty()
                p=S.Popen([str(binary),'--debug',*args],env=env,stdout=slave,stderr=S.PIPE)
                os.close(slave);trace=bytearray()
                def wait_for(marker,stimulate=None):
                    deadline=time.monotonic()+20
                    attempt=0
                    while marker not in trace:
                        assert p.poll()is None,(name,'early exit',p.returncode,bytes(trace))
                        assert time.monotonic()<deadline,(name,'trace timeout',bytes(trace))
                        if stimulate:
                            stimulate(attempt);attempt+=1
                        if select.select([master],[],[],0.1)[0]:
                            data=os.read(master,4096);assert data;trace.extend(data);assert len(trace)<65536
                try:
                    wait_for(b'Hiding the cursor.')
                    # Start-hidden traces precede XI2 selection in upstream.
                    # Keep bounded input flowing until the event loop observes it.
                    def wake(attempt):
                        if wakeup=='motion':assert motion(dpy,0,17+case*9+attempt%%31,23+case*7,0)
                        else:assert button(dpy,1,1,0) and button(dpy,1,0,0)
                        sync(dpy,0)
                    wait_for(b'Showing the cursor.',wake)
                    assert p.poll()is None and trace.count(b'Hiding the cursor.')==1
                    checks.append('xvfb-xi2-trace-'+name)
                finally:
                    if p.poll()is None:p.terminate()
                    try:_,error=p.communicate(timeout=5)
                    except S.TimeoutExpired:p.kill();_,error=p.communicate(timeout=5)
                    os.close(master)
                    assert not error,(name,error)
        finally:
            if dpy:close(dpy)
            os.close(rd)
            if server.poll()is None:server.terminate()
            try:server.wait(timeout=5)
            except S.TimeoutExpired:server.kill();server.wait(timeout=5)
print('UNCLUTTER_QA_OK '+str(len(checks))+' '+','.join(checks))
UNCLUTTER_QA

%build
# Environment flags are extended by the original Makefile += assignments.
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build all

%install
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_install PREFIX=%{_prefix} LICENSEDIR=%{_licensedir}/%{name}
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE

%check
python3 -I -B downstream-qa.py %{buildroot}

%files
%license LICENSE
%doc README.md DEPENDENCIES
%{_bindir}/unclutter
%{_mandir}/man1/unclutter.1*

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_libexecdir}/%{name}-tests
%{_datadir}/%{name}/qa

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.6-1
- Onboard the fixed official release with original defaults and offline checks.
