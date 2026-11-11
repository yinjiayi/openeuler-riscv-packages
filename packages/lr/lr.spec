# SPDX-License-Identifier: Apache-2.0
Name:           lr
Version:        2.0.1
Release:        1%{?dist}
Summary:        Recursive file listing with filtering and formatting
License:        MIT
URL:            https://github.com/leahneukirchen/lr
Source0:        lr-2.0.1.tar.gz
Patch0:         patches/0001-check-input-boundaries.patch
ExclusiveArch:  riscv64
BuildRequires:  gcc make patch coreutils diffutils glibc-devel python3 bash zsh
Requires:       glibc

%description
lr lists files recursively with original configurable ordering, filtering,
formatting, symlink and input-list features, and the default zsh completion.

%package tests
Summary:        Mandatory offline functional tests for lr
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3 bash zsh

%description tests
Bounded offline tests of the installed default executable and exact documentation.

%prep
%autosetup -N -n lr-%{version}
cp -p lr.c downstream-lr-original.c
echo 'ff96f38fab8f67c94415bb295781e318d0a946cbfa823b2c62775af34b9ab748  downstream-lr-original.c' | sha256sum -c -
# Preserve the source's complete original notice, including its newer date.
python3 -I -B - <<'LR_NOTICE'
from pathlib import Path
import hashlib
original = Path('downstream-lr-original.c').read_bytes()
notice = b'/*\n * Copyright' + original.split(b'/*\n * Copyright', 1)[1].split(b' */', 1)[0] + b' */\n'
assert hashlib.sha256(notice).hexdigest() == 'f534d8126d90ccde755ed7e625b94d77c0a15e7b020e9702f696fa7fff6144ee'
Path('SOURCE-NOTICE').write_bytes(notice)
LR_NOTICE
%autopatch -p1
echo 'c5a0f9bdb1145e5eed6c720c3daeced37fd61e03f38c17f247abe04ba84eb7cc  lr.c' | sha256sum -c -
cat > downstream-qa.py <<'LR_QA'
"""Mandatory downstream functional QA; execute only on the hosted target.

This tests the original default executable with isolated file fixtures. The
separate regression driver tests the reviewed boundary patch with instrumented
ordering controls; neither test is a native-performance or general safety proof.
"""
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile


def main():
    assert len(sys.argv) == 2
    binary = str(Path(sys.argv[1]).resolve(strict=True))
    assert os.access(binary, os.X_OK)
    with tempfile.TemporaryDirectory(prefix="lr-functional-") as temporary:
        work = Path(temporary)
        root = work / "tree"
        root.mkdir()
        (work / "home").mkdir()
        (root / ".hidden").mkdir()
        (root / "d/nest").mkdir(parents=True)
        contents = {".secret": b"h", ".hidden/x": b"xx", "a": b"aaa",
                    "b.c": b"bbbbb", "d.z": b"1234567",
                    "space name": b"123456789", "d/deep": b"x" * 11,
                    "d/nest/end": b"x" * 13}
        for name, data in contents.items():
            path = root / name
            path.write_bytes(data)
            path.chmod(0o640)
            os.utime(path, (1700000000, 1700000000))
        (root / "a").chmod(0o750)
        (root / "link").symlink_to("a")
        (root / "dirlink").symlink_to("d", target_is_directory=True)
        (root / "broken").symlink_to("missing")
        env = {"PATH": "/usr/bin:/bin", "HOME": str(work / "home"),
               "LC_ALL": "C", "TZ": "UTC0", "TERM": "dumb"}
        calls = 0

        def run(args, expected=0, data=b"", extra=None, cwd=root):
            nonlocal calls
            calls += 1
            current = dict(env)
            if extra:
                current.update(extra)
            child = subprocess.Popen([binary, *args], cwd=cwd, env=current,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
            try:
                out, err = child.communicate(data, timeout=15)
            except BaseException:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
                raise
            assert child.returncode == expected, (args, child.returncode, out, err)
            if expected == 0:
                assert err == b"", (args, err)
            else:
                assert err, (args, "missing error diagnostic")
            return out

        def lines(args, names, **kwargs):
            expected = b"".join(os.fsencode(name) + b"\n" for name in names)
            actual = run(args, **kwargs)
            assert actual == expected, (args, actual, expected)

        names = sorted([".", ".hidden", "d", "d/nest", "broken", "dirlink", "link", *contents])
        lines([], names)
        lines([""], names)
        lines(["-A"], [name for name in names if name == "." or not name.startswith(".")])
        lines(["-1"], [name for name in names if "/" not in name])
        lines(["-d"], ["."])
        lines(["-t", "type == f"], sorted(contents))
        lines(["-t", "type == f", "-t", "size >= 5"], sorted(name for name, data in contents.items() if len(data) >= 5))
        lines(["-t", "type == f", "-t", 'mtime == "2023-11-14 22:13:20"'], sorted(contents))
        lines(["-e", r"^(a|b[.]c)$"], ["a", "b.c"])
        lines(["-t", 'name == "d" ? (prune && skip) : print'], [name for name in names if name != "d" and not name.startswith("d/")])
        lines(["-t", "type == f", "-os"], sorted(contents, key=lambda name: len(contents[name])))
        lines(["-t", "type == f", "-oS"], sorted(contents, key=lambda name: -len(contents[name])))
        lines(["-s", "d"], [".", "deep", "nest", "nest/end"])
        lines(["-f", r"%%P\n", "d"], [".", "deep", "nest", "nest/end"])
        lines(["-H", "dirlink"], ["dirlink", "dirlink/deep", "dirlink/nest", "dirlink/nest/end"])
        lines(["-L", "dirlink"], ["dirlink", "dirlink/deep", "dirlink/nest", "dirlink/nest/end"])
        lines(["-F", "a", "broken", "d", "link", "-d"], ["a*", "broken@", "d/", "link@"])
        lines(["-f", r"%%f|%%s|%%m|%%y|%%TY-%%Tm-%%Td\n", "a"], ["a|3|0750|f|2023-11-14"])
        lines(["-f", r"%%f|%%l|%%F\n", "link"], ["link|a|@"])
        lines(["-Q", "space name"], ["'space name'"])
        lines(["-P", "space name"], ["$'space name'"])
        lines(["-f", r"%%%%\x41\101\t%%p\n", "a"], ["%%AA\ta"])
        lines(["-B", "-f", r"%%d:%%p\n"], [f"{depth}:{name}" for depth in range(4) for name in names if (0 if name == "." else name.count("/") + 1) == depth])
        walked = [".", ".hidden", ".hidden/x", ".secret", "a", "b.c", "broken", "d", "d/deep", "d/nest", "d/nest/end", "d.z", "dirlink", "link", "space name"]
        lines(["-W"], walked)
        postorder = [".hidden/x", ".hidden", ".secret", "a", "b.c", "broken", "d/deep", "d/nest/end", "d/nest", "d", "d.z", "dirlink", "link", "space name", "."]
        lines(["-W", "-D"], postorder)
        unordered = run(["-U"]).splitlines()
        assert len(unordered) == len(names) and set(unordered) == {os.fsencode(name) for name in names}
        lines(["-"], ["a", "b.c"], data=b"b.c\na\nnot-present\n")
        listing = work / "input-list"
        listing.write_bytes(b"b.c\na\nnot-present\n")
        lines(["@" + str(listing)], ["a", "b.c"])
        nul_expected = b"".join(os.fsencode(name) + b"\0" for name in names)
        assert run(["-0"]) == nul_expected
        assert run(["-0", "-"], data=b"b.c\0a\0") == b"a\0b.c\0"
        strange = work / "strange"
        strange.mkdir()
        odd = strange / "line\nbreak"
        odd.write_bytes(b"x")
        assert run(["-0", str(odd)]) == os.fsencode(odd) + b"\0"
        assert run(["-G", "a"]) == b"a\n"
        assert b"\x1b[" in run(["-GG", "a"])
        assert run(["-GG", "a"], extra={"NO_COLOR": "1"}) == b"a\n"
        assert run(["-X", "a"]) == b"a\n"
        hyperlink = run(["-XX", "a"])
        assert b"\x1b]8;;file://" in hyperlink and os.fsencode(root / "a") in hyperlink
        for args in (["--invalid"], ["-T", "Z"], ["-t", "not-an-expression"],
                     ["-t", "size > 900000000000000000T"],
                     ["-t", 'mtime > "-900000000000000000h"'],
                     ["-f", "%%"], ["-f", "\\"], ["-f", "%%T"]):
            run(args, expected=2)
        run(["not-present"], expected=1)
        print("lr default functional QA passed:", calls, "bounded offline invocations")


if __name__ == "__main__":
    main()
LR_QA
cat > downstream-regression.py <<'LR_REGRESSION'
"""Target-only instrumented source-boundary regression, not allocator/UBSan proof."""
import hashlib,json,pathlib,subprocess,sys
ORIGINAL='ff96f38fab8f67c94415bb295781e318d0a946cbfa823b2c62775af34b9ab748'
FIXED='c5a0f9bdb1145e5eed6c720c3daeced37fd61e03f38c17f247abe04ba84eb7cc'
HEADER=r'''
#define _GNU_SOURCE
#define _FILE_OFFSET_BITS 64
#include <sys/types.h>
#include <sys/xattr.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <assert.h>
static int64_t qa_multiply(int64_t, int64_t);
static int64_t qa_subtract(int64_t, int64_t);
static void qa_days(int *, int64_t);
static void qa_store(char *, size_t, size_t);
static int qa_probe_recurse(char *, void *, int);
static void *qa_malloc(size_t);
static size_t qa_strlen(const char *);
static ssize_t qa_attrs(const char *, char *, size_t);
static void *qa_allocation;
static int qa_xattr_case;
#define main lr_program_main
#define malloc qa_malloc
#define strlen qa_strlen
#define listxattr qa_attrs
#define llistxattr qa_attrs
#include "under-test.c"
#undef main
#undef malloc
#undef strlen
#undef listxattr
#undef llistxattr
static int64_t qa_multiply(int64_t n, int64_t factor) {
 assert(factor > 0);
 if (n > INT64_MAX/factor || n < INT64_MIN/factor) _exit(31);
 return n*factor;
}
static int64_t qa_subtract(int64_t n, int64_t value) {
 if ((value > 0 && n < INT64_MIN+value) ||
     (value < 0 && n > INT64_MAX+value)) _exit(32);
 return n-value;
}
static void qa_days(int *day, int64_t n) {
 if (n > INT_MAX || n < INT_MIN ||
     (n > 0 && *day < INT_MIN+n) ||
     (n < 0 && *day > INT_MAX+n)) _exit(33);
 *day -= n;
}
static void qa_store(char *b, size_t length, size_t index) {
 if (index >= length) _exit(34);
 b[index]=0;
}
static int qa_probe_recurse(char *path, void *history, int guess) {
 (void)path;(void)history;(void)guess;return 0;
}
static void *qa_malloc(size_t size) {
 void *p=malloc(size);assert(p);memset(p,0xa5,size);qa_allocation=p;return p;
}
static size_t qa_strlen(const char *s) {
 if (qa_xattr_case && qa_allocation &&
     s==((struct fileinfo *)qa_allocation)->xattr && s[3]!=0) _exit(35);
 return strlen(s);
}
static ssize_t qa_attrs(const char *path, char *out, size_t size) {
 static const char attrs[]="security.capability\0system.posix_acl_access\0user.qa\0";
 (void)path;assert(size>=sizeof(attrs)-1);memcpy(out,attrs,sizeof(attrs)-1);
 return sizeof(attrs)-1;
}
int main(int argc, char **argv) {
 assert(argc==2);argv0=(char *)"lr-boundary-test";now=1700000000;
 assert(setenv("TZ","UTC0",1)==0);tzset();
 if (!strcmp(argv[1],"numeric-overflow")) {
  int64_t n;char text[]="900000000000000000T";pos=text;parse_num(&n);return 41;
 }
 if (!strcmp(argv[1],"relative-product")) {
  int64_t n;char text[]="\"-900000000000000000h\"";pos=text;parse_dur(&n);return 42;
 }
 if (!strcmp(argv[1],"relative-days")) {
  int64_t n;char text[]="\"-900000000000000000d\"";pos=text;parse_dur(&n);return 43;
 }
 if (!strcmp(argv[1],"relative-negative")) {
  int64_t n;char text[]="\"--9223372036854775807s\"";pos=text;parse_dur(&n);return 44;
 }
 if (!strcmp(argv[1],"relative-nosuffix")) {
  int64_t n;char text[]="\"-12\"";pos=text;parse_dur(&n);return 45;
 }
 if (!strcmp(argv[1],"path-boundary")) {
  char *path=malloc(PATH_MAX+1);assert(path);memset(path,'x',PATH_MAX);path[PATH_MAX]=0;
  errno=0;assert(traverse(path)==-1 && errno==ENAMETOOLONG);free(path);return 0;
 }
 if (!strcmp(argv[1],"xattr-termination")) {
  struct stat st={0};st.st_mode=S_IFREG|0600;need_xattr=1;Uflag=1;
  format=(char *)"";qa_xattr_case=1;callback("fixture",&st,0,0,0);assert(maxxattr==3);return 0;
 }
 if (!strcmp(argv[1],"format-percent") || !strcmp(argv[1],"format-backslash")) {
  char bad_percent[]={'%%',0,'%%','Y',0},bad_backslash[]={'\\',0,'%%','Y',0};
  format=!strcmp(argv[1],"format-percent")?bad_percent:bad_backslash;
  ordering=(char *)"n";analyze_format();assert(need_fstype==1);return 36;
 }
 if (!strcmp(argv[1],"format-time")) {
  struct fileinfo fi={0};char bad[]={'%%','T',0,'Z',0};format=bad;
  print_format(&fi);return 37;
 }
 assert(!strcmp(argv[1],"ordinary"));
 static const struct {const char *text;int64_t want;} cases[]={
  {"0",0},{"123c",123},{"2b",1024},{"3k",3072},
  {"4M",4194304},{"5G",5368709120LL},{"6T",6597069766656LL}};
 for (size_t i=0;i<sizeof(cases)/sizeof(cases[0]);i++) {
  char input[128];snprintf(input,sizeof(input),"%%s",cases[i].text);pos=input;
  int64_t got=-1;assert(parse_num(&got)==1 && got==cases[i].want && !*pos);
 }
 static const struct {const char *text;int64_t delta;} durations[]={
  {"\"-2h\"",7200},{"\"-3m\"",180},{"\"-4s\"",4}};
 for (size_t i=0;i<sizeof(durations)/sizeof(durations[0]);i++) {
  char input[128];snprintf(input,sizeof(input),"%%s",durations[i].text);pos=input;
  int64_t got=0;assert(parse_dur(&got)==1 && got==now-durations[i].delta && !*pos);
 }
 char days[]="\"-2d\"";pos=days;int64_t midnight=0;
 assert(parse_dur(&midnight)==1 && midnight==1699747200 && !*pos);
 char path[PATH_MAX];memset(path,'x',PATH_MAX-1);path[PATH_MAX-1]=0;
 assert(traverse(path)==0);
 format=(char *)"%%p\\n%%TY %%%%";ordering=(char *)"n";analyze_format();
 return 0;
}
'''
def instrument(source,original):
 def rep(old,new,count=1):
  nonlocal source
  assert source.count(old)==count,(old,source.count(old));source=source.replace(old,new)
 if original:
  for factor in ['512LL','1024LL','1024LL * 1024','1024LL * 1024 * 1024','1024LL * 1024 * 1024 * 1024']:
   rep('n *= '+factor+';', 'n = qa_multiply(n, '+factor+');')
  rep('*n = now - (d*60*60);','*n = qa_subtract(now, qa_multiply(d, 3600));')
  rep('*n = now - (d*60);','*n = qa_subtract(now, qa_multiply(d, 60));')
  rep('*n = now - d;','*n = qa_subtract(now, d);')
  rep('tmnow->tm_mday -= d;','qa_days(&tmnow->tm_mday, d);')
 rep('pathbuf[prefixl + 1] = 0;','qa_store(pathbuf, sizeof pathbuf, prefixl + 1);')
 rep('return recurse(pathbuf, 0, 1);','return qa_probe_recurse(pathbuf, 0, 1);')
 return source
def run(command,cwd):
 p=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 return p.returncode,p.stdout,p.stderr
def main():
 assert len(sys.argv)>=5 and sys.argv[1]=='--target-check'
 original,fixed,work=map(pathlib.Path,sys.argv[2:5]);cc=sys.argv[5:];assert cc
 a=original.read_bytes();b=fixed.read_bytes();assert hashlib.sha256(a).hexdigest()==ORIGINAL and hashlib.sha256(b).hexdigest()==FIXED
 work.mkdir(exist_ok=False);results=[]
 for label,data,is_original in [('original',a,True),('fixed',b,False)]:
  out=work/label;out.mkdir();(out/'under-test.c').write_text(instrument(data.decode(),is_original));(out/'driver.c').write_text(HEADER)
  code,stdout,stderr=run(cc+['-UNDEBUG','driver.c','-o','boundary-driver'],out)
  assert code==0,(label,'compile',code,stdout,stderr)
  expected={'ordinary':0,'numeric-overflow':31,'relative-product':31,'relative-days':33,'relative-negative':32,'relative-nosuffix':2,'path-boundary':34,'xattr-termination':35,'format-percent':36,'format-backslash':36,'format-time':37} if is_original else {'ordinary':0,'numeric-overflow':2,'relative-product':2,'relative-days':2,'relative-negative':2,'relative-nosuffix':2,'path-boundary':0,'xattr-termination':0,'format-percent':2,'format-backslash':2,'format-time':2}
  for case,want in expected.items():
   code,stdout,stderr=run([str((out/'boundary-driver').resolve()),case],out)
   assert code==want,(label,case,want,code,stdout,stderr)
   if not is_original and code==2:assert b'parse error:'in stderr,(case,stderr)
   results.append(dict(variant=label,case=case,returncode=code,stdout=stdout.decode(errors='backslashreplace'),stderr=stderr.decode(errors='backslashreplace')))
 print(json.dumps(dict(results=results,boundary='Instrumented target-only ordering/bounds controls, not UBSan/ASan/real allocator or general memory-safety proof.'),sort_keys=True))
if __name__=='__main__':main()
LR_REGRESSION

%build
# Keep original all target, implicit compiler recipe and original warning flags.
%make_build all CC=gcc CFLAGS='%{optflags} -Wall -Wno-switch -Wextra -Wwrite-strings' LDFLAGS='%{?build_ldflags}'

%install
# Original install target installs lr, its manual and default zsh completion.
%make_install PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir} ZSHCOMPDIR=%{_datadir}/zsh/site-functions
install -D -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/lr-tests/qa.py

%check
# No original test/check target exists; none is removed or replaced.
# Assertions are mandatory; -UNDEBUG is last in each target harness compilation.
python3 -I -B downstream-regression.py --target-check downstream-lr-original.c lr.c downstream-regression-work gcc %{optflags} %{?build_ldflags}
python3 -I -B downstream-qa.py ./lr
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/lr
cmp _lr %{buildroot}%{_datadir}/zsh/site-functions/_lr
zsh -n %{buildroot}%{_datadir}/zsh/site-functions/_lr
python3 -I -B - <<'LR_STAGED_MAN'
from pathlib import Path
import gzip
directory = Path('%{buildroot}%{_mandir}/man1')
manuals = list(directory.glob('lr.1*'))
assert len(manuals) == 1 and manuals[0].name in ('lr.1', 'lr.1.gz')
raw = manuals[0].read_bytes()
decoded = gzip.decompress(raw) if manuals[0].name.endswith('.gz') else raw
assert decoded == Path('lr.1').read_bytes()
LR_STAGED_MAN

%files
%license LICENSE SOURCE-NOTICE
%doc README.md NEWS.md
%{_bindir}/lr
%{_mandir}/man1/lr.1*
%{_datadir}/zsh/site-functions/_lr

%files tests
%license LICENSE SOURCE-NOTICE
%{_libexecdir}/lr-tests/

%changelog
* Tue Oct 20 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Preserve default recursive listing and add checked input bounds with target tests.
