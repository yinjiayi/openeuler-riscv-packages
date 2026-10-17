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
    if mode=='installed':assert subprocess.check_output(['rpm','-qf','--qf','%{NAME}',str(p)],text=True)=='c-lolcat'
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
