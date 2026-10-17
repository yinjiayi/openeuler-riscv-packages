# SPDX-License-Identifier: Apache-2.0
Name:           c-lolcat
Version:        1.5
Release:        1%{?dist}
Summary:        Colorful cat and censor command-line tools
License:        WTFPL AND BSD-2-Clause
URL:            https://github.com/jaseg/lolcat
Source0:        c-lolcat-1.5.tar.gz
Source1:        LICENSE-Pygments
Source2:        AUTHORS-Pygments
Patch0:         0001-use-python3-for-original-table-generator.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  patch
BuildRequires:  gzip
BuildRequires:  tar

%description
Original C implementation of colorful cat plus the default censor tool.
The root Makefile's default all and install targets are retained. Runtime
depends on libc and libm; Python is only generator and test support.

%prep
%setup -q -n lolcat-a9ab81839f2a00fa1d831648a1d79e268bb1ddac
test ! -e ../c-lolcat-pristine
mkdir ../c-lolcat-pristine
cp -a . ../c-lolcat-pristine/
printf '95ba74a1a557eda92c389fa6e7e88b99224709d5f3097a330c4f3f6c15544e16  Makefile\n' | sha256sum --check --strict
%patch -P 0 -p1
cp %{SOURCE1} LICENSE-Pygments
cp %{SOURCE2} AUTHORS-Pygments
cat > BORROWED-NOTICE <<'NOTICE'
The upstream xterm256lut_gen.py states "This is ripped out of pygments".
Conservatively retain the complete Pygments BSD license and AUTHORS.
Pygments terminal256 formatter: Copyright 2006-2025 by the Pygments team.
Its RGB-to-XTERM routines credit adaptation from xterm256-conv by
Wolfgang Frisch. This notice preserves that attribution without claiming
that Pygments 2.19.2 is the exact historical copied version.
Notice files are pinned to official pygments/pygments commit
cfca62e6e95136e48a255e8cbffb0bbe1d98456c (stable tag 2.19.2).
The original jaseg/lolcat WTFPL notices and all source bytes are retained.
NOTICE

%build
# Regenerate the original table in target CI, never execute it on the local host.
rm -f xterm256lut.h
%make_build CC=gcc CFLAGS="%{optflags} -std=c11 -Wall -Wextra -Wno-sign-compare"
printf '7e0d41fdaa9558663fb333fd825c2aa95b2b40afca8562ff018154d8f971b332  xterm256lut.h\n' | sha256sum --check --strict

%install
install -d %{buildroot}%{_bindir}
%make_install DESTDIR=%{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/c-lolcat/original
cp -a ../c-lolcat-pristine/. %{buildroot}%{_datadir}/c-lolcat/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/c-lolcat/c-lolcat-1.5.tar.gz
install -m 0644 LICENSE-Pygments AUTHORS-Pygments BORROWED-NOTICE %{buildroot}%{_datadir}/c-lolcat/
cat > %{buildroot}%{_datadir}/c-lolcat/original-files.json <<'JSON'
{".gitignore":"10664009389ded9469e8fa89bb3aa1eacdb6d8016b29e38196fd7c957ea330d4",".gitmodules":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","LICENSE":"cd07c1b44b0486d0aa498e0aa17a62a06e0e566f9e85853f8c38b7fc52c6d03e","LOLCat-Rainbow.jpg":"9d6be3d49b2f540dc8553101ed6b1428360abbd67a81fb075f2fd94e772aba01","Makefile":"95ba74a1a557eda92c389fa6e7e88b99224709d5f3097a330c4f3f6c15544e16","PKGBUILD":"f37f6ed6a81b96c58bcddaaf7888083edf0d4268def5d16f84155c2a312d5e36","README.md":"5ab391c046634d481612c2caffea3aa56c29ac5995b3eb60cab464ae95411e97","autotools/Makefile.am":"266262d68653e84c48f5c9ab74d31a28d75cca47e8ba40affb9719b0484fa959","autotools/README":"c31996f9b1f31855b77af5e13ee99827a0e77c1ecd0c3a09123e65f66d11ee2f","autotools/autogen.sh":"8ac3704cdf8c8f749973c411113f12bd3853f657aa547879d3a4b2d74a582b25","autotools/configure.ac":"06995df777d15d78989bf9ad569f1b1270e366d5c3ae2906d8b4114034bcd195","censor.c":"5f899dadb0d8e88857c9d03eed320b6d06e41c952931d48ead67d1a301b3ce56","lolcat.c":"cf5bf95f5879212ecbff5532b9e6c57232169aabd176edea6d59f2fe1717c44c","screenshot.png":"9ee8405a4012c7e8f5f37a65f63069cedfbb40e316a893d3fb3a32b1fac9d738","sl.gif":"ae27df97ce7470d3278de712cd6a8eb234ffb379ccd5c831d1b3bc1579b1cfa2","xterm256lut.h":"7e0d41fdaa9558663fb333fd825c2aa95b2b40afca8562ff018154d8f971b332","xterm256lut_gen.py":"aa200e21bfca0bab89d7f79952127d0f0b561217dfc31a60d86d7a63e62f891c"}
JSON

%check
# Upstream has no check/test target. This is a separate downstream CLI smoke.
cat > c-lolcat-cli.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
python3 -I - "$@" <<'PY'
import hashlib,json,os,pathlib,re,subprocess,sys,tempfile
assert len(sys.argv) in (1,4)
mode='installed' if len(sys.argv)==1 else sys.argv[3]
assert mode in ('staged','installed')
root=pathlib.Path(sys.argv[1]).resolve() if mode=='staged' else pathlib.Path('/')
share=pathlib.Path(sys.argv[2]).resolve() if mode=='staged' else pathlib.Path('/usr/share/c-lolcat')
manifest=json.loads((share/'original-files.json').read_bytes())
assert len(manifest)==17
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if mode=='installed':assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='c-lolcat'
def physical(p):
    assert p.is_file() and not p.is_symlink()
    p.resolve().relative_to(root)
    owned(p)
for path,h in manifest.items():
    p=share/'original'/path;physical(p);assert sha(p)==h
assert {p.relative_to(share/'original').as_posix() for p in (share/'original').rglob('*') if p.is_file()}==set(manifest)
for path,h in {
    'c-lolcat-1.5.tar.gz':'97860debda5631417df11dc7dd617af969e740eeffd9b41e4aa228d303aa48bc',
    'LICENSE-Pygments':'a9d66f1d526df02e29dce73436d34e56e8632f46c275bbdffc70569e882f9f17',
    'AUTHORS-Pygments':'0660e318a6f215802adc8731ab85d0c65ff27cfcca3f5d28597f306476195bd9',
}.items():
    p=share/path;physical(p);assert sha(p)==h
physical(share/'original-files.json')
physical(share/'BORROWED-NOTICE')
binaries={name:root/'usr/bin'/name for name in ('lolcat','censor')}
origins={}
for name,p in binaries.items():
    physical(p);b=p.read_bytes()
    assert b[:6]==b'\x7fELF\x02\x01' and int.from_bytes(b[18:20],'little')==243
    origins[name]=dict(path=str(p),sha256=sha(p),elf_machine=243)
env={k:v for k,v in os.environ.items() if not k.startswith('LD_')}
env.update(LC_ALL='C.UTF-8',LANG='C.UTF-8')
reports=[]
def run(name,args,input=None,expected=0):
    argv=[str(binaries[name]),*args]
    q=subprocess.run(argv,input=input,env=env,capture_output=True,timeout=30)
    assert q.returncode==expected,(argv,q.returncode,q.stderr)
    reports.append(dict(argv=argv,returncode=q.returncode,stdout_sha256=hashlib.sha256(q.stdout).hexdigest(),stderr_sha256=hashlib.sha256(q.stderr).hexdigest()))
    return q.stdout,q.stderr
ascii=b'abc XYZ 9.\n'
unicode='Hello 世界 café\n'.encode()
for value in (ascii,unicode):
    out,err=run('lolcat',[],value);assert out==value and err==b''
out,err=run('lolcat',['--version']);assert b'lolcat version 1.5,' in out and err==b''
out,err=run('lolcat',['--help']);assert b'Usage:' in out and b'lolcat' in out and err==b''
strip=lambda b:re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]',b'',b)
for options in (['-f'],['-f','-x'],['-f','-b'],['-f','-g','ff0000:0000ff']):
    out,err=run('lolcat',[*options,'-S','1'],ascii)
    assert b'\x1b[' in out and strip(out)==ascii and err==b''
with tempfile.TemporaryDirectory(prefix='c-lolcat-cli-smoke-') as tmp:
    work=pathlib.Path(tmp);one=work/'one';two=work/'two'
    one.write_bytes(ascii);two.write_bytes(unicode)
    out,err=run('lolcat',[str(one),str(two)]);assert out==ascii+unicode and err==b''
    out,err=run('lolcat',[str(one),'-'],unicode);assert out==ascii+unicode and err==b''
    missing=str(work/'missing')
    out,err=run('lolcat',[missing],expected=2);assert b'Cannot open' in err
    out,err=run('censor',[missing],expected=2);assert b'Cannot open' in err
out,err=run('lolcat',['-h','invalid'],ascii,2);assert b'Usage:' in out+err
out,err=run('lolcat',['-b','-x'],ascii,2);assert b'Usage:' in out+err
expected='▄█▄ ███ █.\n'.encode()
out,err=run('censor',[],ascii);assert out==expected and err==b''
out,err=run('censor',[],b'\x1b[31m'+ascii+b'\x1b[0m');assert out==b'\x1b[31m'+expected+b'\x1b[0m' and err==b''
for name,p in binaries.items():assert sha(p)==origins[name]['sha256']
for path,h in manifest.items():assert sha(share/'original'/path)==h
assert len(reports)==16
print('C_LOLCAT_CLI_RESULT='+json.dumps(dict(mode=mode,origins=origins,commands=reports,original_files=17,upstream_test_target=None,boundary='Original root make all/install both tools and original generated table preserved; downstream non-TTY/forced-color CLI checks only. No upstream test suite, interactive TTY, native or performance assertion.')))
PY
SH
/bin/bash c-lolcat-cli.sh "%{buildroot}" "%{buildroot}%{_datadir}/c-lolcat" staged

%files
%license LICENSE LICENSE-Pygments AUTHORS-Pygments BORROWED-NOTICE
%doc README.md
%{_bindir}/lolcat
%{_bindir}/censor
%{_datadir}/c-lolcat/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Preserve both original default tools and original color-table generation.
- Retain conservative Pygments BSD attribution and complete originals.
- Add fail-closed staged and installed CLI behavior/origin checks.
