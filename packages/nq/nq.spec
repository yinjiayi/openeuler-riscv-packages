# SPDX-License-Identifier: CC0-1.0
Name:           nq
Version:        1.0
Release:        1%{?dist}
Summary:        Lightweight command-line job queue utilities
License:        CC0-1.0
URL:            https://github.com/leahneukirchen/nq
Source0:        nq-1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  perl-Test-Harness
BuildRequires:  python3
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  bash
Requires:       /bin/sh
Recommends:     tmux
Recommends:     screen

%description
The original nq job queue, nqtail log follower and nqterm terminal wrapper.
Queues use ordinary user-writable directories and POSIX file locking.

%package tests
Summary:        Original nq TAP tests and installed-package checks
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       perl-Test-Harness
Requires:       coreutils
Requires:       grep
Requires:       sed
Requires:       /bin/sh

%description tests
Unmodified upstream TAP suite and bounded installed-package checks. These test
ordinary userspace behavior, not native scheduling, kernel timing, performance,
multi-user security or interactive tmux/screen sessions.

%prep
%setup -q -n nq-2bb551efd8b3e50d715482a8f3b89f88bae74397
cat > downstream-qa.py <<'NQ_QA'
# SPDX-License-Identifier: CC0-1.0
# Copyright 2026 yinjiayi; dedicated to the public domain under CC0-1.0.
"""Original TAP suite plus bounded userspace checks; no native timing claim."""
import hashlib
import os
from pathlib import Path
import re
import subprocess as S
import sys
import tarfile
import tempfile

root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/nq';tail=root/'usr/bin/nqtail';wrapper=root/'usr/bin/nqterm'
archive=root/'usr/share/nq/qa/nq-1.0.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='58dcec1ffda79272c87984f9727e748f3d7758030a7b7c9c8440fc4006bd3fb2'
with tarfile.open(archive,'r:gz')as tf:
    members=[m for m in tf.getmembers()if m.isfile()];assert len(members)==15
    original={m.name.split('/',1)[1]:tf.extractfile(m).read()for m in members}
    testmode=next(m.mode for m in members if m.name.endswith('/tests'))
license_=original['COPYING'];assert b'Leah Neukirchen'in license_ and b'creativecommons.org/publicdomain/zero/1.0/'in license_
for name in ('nq','nq-tests'):
    assert(root/'usr/share/licenses'/name/'COPYING').read_bytes()==license_
for name in ('README.md','NEWS.md'):
    assert(root/'usr/share/doc/nq'/name).read_bytes()==original[name]
assert original['nqterm']==wrapper.read_bytes()
assert b"printf '1..36\\n'"in original['tests']
checks=['original-15-member-archive-and-CC0-notices']
with tempfile.TemporaryDirectory(prefix='nq-qa-')as temporary:
    work=Path(temporary);(work/'tests').write_bytes(original['tests']);(work/'tests').chmod(testmode&0o777)
    env={'PATH':str(binary.parent)+':/usr/bin:/bin','HOME':temporary,'LC_ALL':'C','NQ':str(binary),'NQTAIL':str(tail)}
    p=S.run(['/usr/bin/prove','-v','./tests'],cwd=work,env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=180)
    sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
    assert p.returncode==0,(p.returncode,p.stdout,p.stderr)
    assert len(re.findall(rb'^ok - ',p.stdout,re.M))==36 and b'All tests successful.'in p.stdout and not re.search(rb'^not ok',p.stdout,re.M)
    assert not(work/'test.dir').exists();checks.append('unmodified-upstream-36-TAP-cases')
    p=S.run([str(binary),'-h'],cwd=work,env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==1 and not p.stdout and p.stderr==b'usage: nq [-c] [-q] [-w ... | -t ... | CMD...]\n'
    checks.append('original-nq-help-status-and-stderr')
    p=S.run([str(tail),'-Q'],cwd=work,env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==1 and not p.stdout and b'usage: nqtail [-anq] [JOBID...]\n'in p.stderr
    checks.append('original-nqtail-invalid-option')
    queue=work/'wrapper-queue';queue.mkdir();env['NQDIR']=str(queue)
    p=S.run([str(wrapper),'/bin/echo','nq-installed-wrapper'],cwd=work,env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=15)
    assert p.returncode==0 and not p.stderr and re.fullmatch(rb',[0-9a-f]+\.[0-9]+\n',p.stdout)
    job=p.stdout.decode().strip()
    p=S.run([str(binary),'-w',job],cwd=work,env=env,stdin=S.DEVNULL,stdout=S.PIPE,stderr=S.PIPE,timeout=20)
    assert p.returncode==0 and not p.stdout and not p.stderr and b'\nnq-installed-wrapper\n'in(queue/job).read_bytes()
    checks.append('original-nqterm-without-multiplexer')
print('NQ_QA_OK '+str(len(checks))+' '+','.join(checks))
NQ_QA

%build
# Keep original default all and -Wall -O2, adding normal RPM hardening/debug.
%make_build all CC=gcc CFLAGS="%{optflags} -Wall -O2" LDFLAGS="%{?build_ldflags}"

%install
%make_install PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir} CC=gcc CFLAGS="%{optflags} -Wall -O2" LDFLAGS="%{?build_ldflags}"
install -Dm 0644 COPYING %{buildroot}%{_licensedir}/%{name}/COPYING
install -Dm 0644 COPYING %{buildroot}%{_licensedir}/%{name}-tests/COPYING
install -Dm 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -Dm 0644 NEWS.md %{buildroot}%{_docdir}/%{name}/NEWS.md
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# Original target: all 36 assertions, shell/PID checks and sleeps retained.
make check CC=gcc CFLAGS="%{optflags} -Wall -O2" LDFLAGS="%{?build_ldflags}"
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/COPYING
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/NEWS.md
%{_bindir}/nq
%{_bindir}/nqtail
%{_bindir}/nqterm
%{_mandir}/man1/nq.1*
%{_mandir}/man1/nqtail.1*
%{_mandir}/man1/nqterm.1*

%files tests
%license %{_licensedir}/%{name}-tests/COPYING
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0-1
- Onboard fixed official v1.0 with unchanged defaults and original TAP suite.
