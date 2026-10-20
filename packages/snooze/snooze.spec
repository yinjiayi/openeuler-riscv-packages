# SPDX-License-Identifier: Apache-2.0
Name:           snooze
Version:        0.6
Release:        1%{?dist}
Summary:        Run a command at a particular time
License:        CC0-1.0
URL:            https://github.com/leahneukirchen/snooze
Source0:        snooze-0.6.tar.gz
Patch0:         patches/0001-check-duration-before-multiplication.patch
ExclusiveArch:  riscv64
BuildRequires:  gcc make patch coreutils diffutils glibc-devel python3 bash
Requires:       glibc

%description
Snooze runs a command when all specified date fields match, with original
timefile, slack, random delay, jitter, dry-run, SIGALRM and SIGCONT support.

%package tests
Summary:        Mandatory offline functional tests for snooze
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3 bash

%description tests
Bounded tests of the installed ordinary executable and exact original notices.

%prep
%autosetup -N -n snooze-53e4afe05aaa953370141156fbeb9fc21979e9e0
mkdir downstream-original
cp -p snooze.c downstream-original/snooze.c
echo '50c51015ace7ae71e2d5d3e4fae5176d901294efcfb99aa8ca8b9720499cc4a1  downstream-original/snooze.c' | sha256sum -c -
patch --fuzz=0 -p1 -i %{PATCH0}
echo '2d1aa70ed4a2c0100e590cadc2d1c23001ab207bedd557f2ec893426a013fd12  snooze.c' | sha256sum -c -
cat > downstream-qa.py <<'SNOOZE_QA'
"""Mandatory bounded target-only Snooze functional QA; no clock-precision claim.

Execute the ordinary binary, not a model or replacement. Calendar/parser unit
controls and original-negative duration controls run separately in target check.
The same binary QA runs built, staged, and installed. No wall clock is changed.
"""
import datetime as dt
import gzip
import hashlib
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time


def main():
    assert len(sys.argv) in (2,3)
    binary=str(Path(sys.argv[1]).resolve(strict=True))
    env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC0'}
    allseconds=['-H','*','-M','*','-S','*']
    calls=0
    with tempfile.TemporaryDirectory(prefix='snooze-functional-') as temporary:
        work=Path(temporary)
        def run(args,status=0):
            nonlocal calls
            calls+=1
            p=subprocess.Popen([binary,*args],cwd=work,env=env,
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:out,err=p.communicate(timeout=15)
            except BaseException:
                os.killpg(p.pid,signal.SIGKILL);p.communicate();raise
            assert p.returncode==status,(args,p.returncode,out,err)
            if status==0:assert not err,(args,err)
            else:assert err,(args,'missing error diagnostic')
            return out

        def dry(args=()):
            before=int(time.time());out=run(['-n',*args]);after=int(time.time())
            dates=[]
            for line in out.decode().splitlines():
                match=re.match(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+0000) ',line)
                if match:dates.append(dt.datetime.strptime(match[1],'%%Y-%%m-%%dT%%H:%%M:%%S%%z'))
            assert len(dates)==5 and dates==sorted(set(dates)),(args,out)
            return before,after,dates,out

        before,after,dates,_=dry(allseconds)
        assert before+1<=dates[0].timestamp()<=after+1
        assert all((b-a).total_seconds()==1 for a,b in zip(dates,dates[1:]))
        _,_,dates,_=dry()
        assert all(x.hour==x.minute==x.second==0 for x in dates)
        assert all((b-a).days==1 for a,b in zip(dates,dates[1:]))
        _,_,dates,_=dry(['-w','7'])
        assert all(x.weekday()==6 and x.hour==x.minute==x.second==0 for x in dates)
        assert all((b-a).days==7 for a,b in zip(dates,dates[1:]))
        _,_,dates,_=dry(['-H','1,3,5','-M','2-4','-S','*/10'])
        assert all(x.hour in (1,3,5) and 2<=x.minute<=4 and x.second%%10==0 for x in dates)
        _,_,dates,_=dry(['-w','1-5','-H','*','-M','*','-S','*/15'])
        assert all(x.weekday()<5 and x.second%%15==0 for x in dates)
        # Invalid fields, reversed/empty/trailing-comma and out-of-range duration.
        for args in (['-H','24'],['-M','60'],['-S','60'],['-w','8'],
                     ['-d','0'],['-m','13'],['-D','367'],['-W','54'],
                     ['-H','3-1'],['-H',''],['-H','1,'],['-H','1x'],
                     ['-H','*/0'],['-s','367d'],['-T','8785h'],
                     ['-R','307445734561825861m'],['-J','213503982334602d']):
            run(['-n',*args],1)
        run(['-?'],2)
        # Timefile min-wait uses mtime+1+T, and does not modify the timefile.
        marker=work/'timefile';stamp=int(time.time())+120
        marker.write_bytes(b'unchanged-timefile\n');os.utime(marker,(stamp,stamp))
        _,_,dates,_=dry([*allseconds,'-t',str(marker),'-T','3'])
        assert dates[0].timestamp()==stamp+4
        assert marker.read_bytes()==b'unchanged-timefile\n' and marker.stat().st_mtime==stamp
        # Missing timefile is overdue; -s0 yields an immediate dry-run date.
        before,after,dates,_=dry([*allseconds,'-s','0','-t',str(work/'missing'),'-T','3'])
        assert before<=dates[0].timestamp()<=after
        # Past timefile without T respects slack, rescheduling to its lower bound.
        stamp=int(time.time())-120;os.utime(marker,(stamp,stamp))
        before,after,dates,_=dry([*allseconds,'-t',str(marker),'-s','2'])
        assert before-1<=dates[0].timestamp()<=after-1
        # Random R is actually evaluated; J dry-run preserves scheduled times.
        before,after,dates,out=dry([*allseconds,'-v','-R','3','-J','2'])
        delay=re.search(rb'^randomly delaying by ([0-3])s\.$',out,re.M);assert delay,out
        assert before+1+int(delay[1])<=dates[0].timestamp()<=after+1+int(delay[1])
        assert out.count(b'(plus up to 2s for jitter)')==5

        def triggered(command,status,expected_output):
            nonlocal calls
            calls+=1
            # Force a schedule beyond two days, including a midnight boundary.
            # This does not change the clock or replace the ordinary binary.
            future=work/('future-'+str(calls));future.write_bytes(b'future\n')
            future_stamp=int(time.time())+2*86400
            os.utime(future,(future_stamp,future_stamp))
            child=subprocess.Popen([binary,'-v','-t',str(future),'-T','0',*command],cwd=work,env=env,
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:
                deadline=time.monotonic()+10
                # Read the actual guest's line-buffered scheduling diagnostic,
                # not only host /proc signal dispositions (QEMU may own those).
                ready=selectors.DefaultSelector();ready.register(child.stdout,selectors.EVENT_READ)
                prefix=b''
                while b'\n'not in prefix:
                    assert time.monotonic()<deadline,'no scheduling diagnostic'
                    if ready.select(.05):
                        chunk=os.read(child.stdout.fileno(),4096);assert chunk
                        prefix+=chunk
                    assert child.poll()is None
                ready.close();assert b'Snoozing until 'in prefix,prefix
                bits=(1<<(signal.SIGALRM-1))|(1<<(signal.SIGCONT-1))
                while True:
                    assert child.poll() is None
                    state=Path('/proc',str(child.pid),'status').read_text()
                    match=re.search(r'^SigCgt:\s*([0-9a-fA-F]+)$',state,re.M);assert match,state
                    if int(match[1],16)&bits==bits:break
                    assert time.monotonic()<deadline,'signal handlers not installed'
                    time.sleep(.01)
                os.kill(child.pid,signal.SIGCONT)
                time.sleep(.05);assert child.poll() is None,'SIGCONT must reschedule, not execute'
                os.kill(child.pid,signal.SIGALRM)
                out,err=child.communicate(timeout=10)
                out=prefix+out
                assert child.returncode==status,(child.returncode,out,err)
                assert b'Snoozing until 'in out and b'Starting execution at 'in out,out
                if status!=255:assert err==b'',err
                else:assert b'execvp:'in err,err
                assert expected_output in out,(expected_output,out)
            finally:
                if child.poll() is None:os.killpg(child.pid,signal.SIGKILL);child.communicate()
        triggered([],0,b'Starting execution at ')
        triggered(['/usr/bin/python3','-c','import sys;print(repr(sys.argv[1:]));sys.exit(37)','space arg','-n'],37,b"['space arg', '-n']\n")
        triggered([str(work/'no-such-command')],255,b'Starting execution at ')
        # Real timed execution with configured jitter; generous bound is functional,
        # not a performance/precision assertion or actual clock-change validation.
        started=time.monotonic()
        out=run([*allseconds,'-J','1','/usr/bin/python3','-c','print("scheduled-command")'])
        assert out==b'scheduled-command\n' and time.monotonic()-started<15
        if len(sys.argv)==3:
            prefix=Path(sys.argv[2])
            for rel,digest in DOCUMENTS.items():
                assert hashlib.sha256((prefix/rel).read_bytes()).hexdigest()==digest,rel
            manual=list((prefix/'usr/share/man/man1').glob('snooze.1*'))
            assert len(manual)==1 and manual[0].name in ('snooze.1','snooze.1.gz'),manual
            raw=manual[0].read_bytes();raw=gzip.decompress(raw)if manual[0].suffix=='.gz'else raw
            assert hashlib.sha256(raw).hexdigest()==MANUAL
    print('snooze-functional: all mandatory groups passed; invocations='+str(calls))


# Proposal emitter replaces these exact placeholders using original source bytes.
DOCUMENTS={'usr/share/doc/snooze/README.md': '03e115dde66bdee7f8d5a013d9edff2ca4ff0c720a2fe765cbbcb4c4e461b021', 'usr/share/doc/snooze/NEWS.md': '6b9fc15dab4561ea4a33cf3a52b7d898b102dd1a5d3701e75b1038e49aff21e8', 'usr/share/licenses/snooze/README.md': '03e115dde66bdee7f8d5a013d9edff2ca4ff0c720a2fe765cbbcb4c4e461b021', 'usr/share/licenses/snooze-tests/README.md': '03e115dde66bdee7f8d5a013d9edff2ca4ff0c720a2fe765cbbcb4c4e461b021'}
MANUAL='2ad59e500732ff02ea48e06d2597250b9156c4c7fc62ee0cd488c3ce04d7b156'
if __name__=='__main__':main()

SNOOZE_QA
cat > downstream-duration.c <<'SNOOZE_DURATION_C'
/* Target-only direct parser regression, original source unchanged. */
#define main snooze_original_main
#include "snooze.c"
#undef main
int main(int argc, char **argv)
{
    if (argc != 2)
        return 99;
    printf("%%ld\n", parse_dur(argv[1]));
    return 0;
}

SNOOZE_DURATION_C
cat > downstream-duration.py <<'SNOOZE_DURATION_PY'
#!/usr/bin/python3
"""Run only inside the target build: compare original and patched parsers."""
import subprocess,sys
original,fixed=sys.argv[1:]
def run(binary,arg):
    return subprocess.run([binary,arg],capture_output=True,timeout=5,check=False)
def exact(binary,arg,status,out,err):
    p=run(binary,arg)
    assert (p.returncode,p.stdout,p.stderr)==(status,out,err),(binary,arg,p.returncode,p.stdout,p.stderr)
# Both original/fixed retain all meaningful small and boundary inputs exactly.
valid={'0':0,'1':1,'31622400':31622400,'0m':0,'1m':60,
       '527040m':31622400,'8784h':31622400,'366d':31622400,
       '+1m':60,' 1m':60}
for binary in (original,fixed):
    for arg,value in valid.items():exact(binary,arg,0,(str(value)+'\n').encode(),b'')
    for arg in ('31622401','527041m','8785h','367d'):
        exact(binary,arg,1,b'',('duration out of range: '+arg+'\n').encode())
    for arg,err in {'':'invalid duration: \'\'\n','x':"invalid duration: 'x'\n",
                    '1s':'junk after duration: s\n','1mm':'junk after duration: m\n'}.items():
        exact(binary,arg,1,b'',err.encode())
# Unsigned-long overflow negative controls are RV64-specific and mandatory.
# They are intentionally accepted by the exact original parser, not skipped.
for arg,wrapped in {'307445734561825861m':44,'213503982334602d':61184}.items():
    exact(original,arg,0,(str(wrapped)+'\n').encode(),b'')
    exact(fixed,arg,1,b'',('duration out of range: '+arg+'\n').encode())
print('duration-parser: original controls and fixed checks passed')

SNOOZE_DURATION_PY
cat > downstream-calendar.c <<'SNOOZE_CALENDAR_C'
/* Target-only actual-source calendar/parser unit controls, not a time model. */
#define main snooze_original_main
#include "snooze.c"
#undef main

static time_t
utc(int year, int mon, int day, int h, int min, int sec)
{
	struct tm tm = { .tm_year = year - 1900, .tm_mon = mon - 1,
	    .tm_mday = day, .tm_hour = h, .tm_min = min, .tm_sec = sec,
	    .tm_isdst = 0 };
	return mktime(&tm);
}

static void
defaults(void)
{
	memset(weekday, '*', sizeof weekday);
	memset(dayofmonth, '*', sizeof dayofmonth);
	memset(month, '*', sizeof month);
	memset(dayofyear, '*', sizeof dayofyear);
	memset(weekofyear, '*', sizeof weekofyear);
	memset(hour, 0, sizeof hour); hour[0] = '*';
	memset(minute, 0, sizeof minute); minute[0] = '*';
	memset(second, 0, sizeof second); second[0] = '*';
	jitter = 0;
}

int
main(int argc, char **argv)
{
	if (setenv("TZ", "UTC0", 1) != 0)
		return 98;
	tzset();
	if (argc == 3 && strcmp(argv[1], "parse") == 0) {
		char result[24];
		parse(argv[2], result, sizeof result, 0);
		for (size_t i = 0; i < sizeof result; i++)
			if (result[i] == '*') printf("%%zu,", i);
		puts("");
		return 0;
	}
	if (argc != 2 || strcmp(argv[1], "calendar") != 0)
		return 99;
	defaults();
	if (find_next(utc(2024, 2, 28, 23, 59, 59)) != utc(2024, 2, 29, 0, 0, 0)) return 1;
	defaults(); parse("29", dayofmonth, sizeof dayofmonth, -1);
	parse("2", month, sizeof month, -1);
	if (find_next(utc(2024, 1, 1, 0, 0, 0)) != utc(2024, 2, 29, 0, 0, 0)) return 2;
	defaults(); parse("60", dayofyear, sizeof dayofyear, -1);
	if (find_next(utc(2024, 1, 1, 0, 0, 0)) != utc(2024, 2, 29, 0, 0, 0)) return 3;
	defaults(); parse("1", weekofyear, sizeof weekofyear, -1);
	if (find_next(utc(2023, 12, 31, 0, 0, 0)) != utc(2024, 1, 1, 0, 0, 0)) return 4;
	defaults(); parse("13", dayofmonth, sizeof dayofmonth, -1);
	parse("5", weekday, sizeof weekday, 0);
	if (find_next(utc(2024, 1, 1, 0, 0, 0)) != utc(2024, 9, 13, 0, 0, 0)) return 5;
	defaults(); parse("30", dayofmonth, sizeof dayofmonth, -1);
	parse("2", month, sizeof month, -1);
	if (find_next(utc(2024, 1, 1, 0, 0, 0)) != (time_t)-1) return 6;
	puts("calendar: leap-day/yday/ISO-week/conjunction/impossible passed");
	return 0;
}

SNOOZE_CALENDAR_C
cat > downstream-calendar.py <<'SNOOZE_CALENDAR_PY'
"""Target-only original/fixed whole-source parser/calendar controls."""
import subprocess
import sys

assert len(sys.argv)==3
cases={'*':range(24),'1,3,5':[1,3,5],'2-4':[2,3,4],
       '*/4':range(0,24,4),'/4':range(0,24,4),'2/5':range(2,24,5),
       '1-10,15/5,23':[*range(1,11),15,20,23]}
for binary in sys.argv[1:]:
    for expr,values in cases.items():
        p=subprocess.run([binary,'parse',expr],capture_output=True,timeout=5)
        expected=(''.join(str(x)+','for x in values)+'\n').encode()
        assert (p.returncode,p.stdout,p.stderr)==(0,expected,b''),(expr,p.returncode,p.stdout,p.stderr)
    for expr in ('','24','-1','3-1','1,','1x','*/0'):
        p=subprocess.run([binary,'parse',expr],capture_output=True,timeout=5)
        assert p.returncode==1 and not p.stdout and p.stderr,(expr,p.returncode,p.stdout,p.stderr)
    p=subprocess.run([binary,'calendar'],capture_output=True,timeout=10)
    assert (p.returncode,p.stdout,p.stderr)==(0,b'calendar: leap-day/yday/ISO-week/conjunction/impossible passed\n',b''),(p.returncode,p.stdout,p.stderr)
print('calendar-parser: original and fixed actual-source controls passed')

SNOOZE_CALENDAR_PY
# Quoted includes search the harness directory first: copies are mandatory.
cp -p downstream-duration.c downstream-original/duration-parser.c
cp -p downstream-calendar.c downstream-original/calendar-parser.c

%build
# Keep the complete upstream default warning/optimization flags and all target.
make %{?_smp_mflags} CC="%{__cc}"

%check
echo '50c51015ace7ae71e2d5d3e4fae5176d901294efcfb99aa8ca8b9720499cc4a1  downstream-original/snooze.c' | sha256sum -c -
echo '2d1aa70ed4a2c0100e590cadc2d1c23001ab207bedd557f2ec893426a013fd12  snooze.c' | sha256sum -c -
%{__cc} -g -O2 -Wall -Wextra -Wwrite-strings downstream-original/duration-parser.c -o duration-original
%{__cc} -g -O2 -Wall -Wextra -Wwrite-strings downstream-duration.c -o duration-fixed
%{__cc} -g -O2 -Wall -Wextra -Wwrite-strings downstream-original/calendar-parser.c -o calendar-original
%{__cc} -g -O2 -Wall -Wextra -Wwrite-strings downstream-calendar.c -o calendar-fixed
python3 -I -B downstream-duration.py ./duration-original ./duration-fixed
python3 -I -B downstream-calendar.py ./calendar-original ./calendar-fixed
python3 -I -B downstream-qa.py ./snooze

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} CC="%{__cc}"
install -D -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/snooze-tests/qa.py
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/snooze
cmp snooze %{buildroot}%{_bindir}/snooze
cmp snooze.1 %{buildroot}%{_mandir}/man1/snooze.1

%files
%license README.md
%doc README.md NEWS.md
%{_bindir}/snooze
%{_mandir}/man1/snooze.1*

%files tests
%license README.md
%dir %{_libexecdir}/snooze-tests
%{_libexecdir}/snooze-tests/qa.py

%changelog
* Tue Oct 20 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.6-1
- Preserve upstream defaults with checked duration arithmetic and mandatory QA.
