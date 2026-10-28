# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 openEuler RISC-V package contributors
Name:           pdfresurrect
Version:        0.23
Release:        1%{?dist}
Summary:        Inspect classic PDF revision history and extract revision selectors
License:        BSD-3-Clause AND Apache-2.0
URL:            https://github.com/enferex/pdfresurrect
# Official source URL: https://api.github.com/repos/enferex/pdfresurrect/tarball/refs/tags/v0.23
Source0:        pdfresurrect-0.23.tar.gz
# Official legal URL: https://www.apache.org/licenses/LICENSE-2.0.txt
Source1:        Apache-2.0.txt
Patch0:         0001-preserve-CFLAGS-in-compiler-checks.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  python3
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       glibc
Requires:       python3

%description
Pdfresurrect inspects revision information in classic PDF files and can copy
the original file with a selected cross-reference trailer. This does not
scrub confidential information and is not a security or rendering validator.
The original experimental scrub feature remains disabled.

%prep
%setup -q -n enferex-pdfresurrect-7a57bff
python3 - <<'PY_ORIGINALS'
import hashlib,json,stat
from pathlib import Path
original = {'.gitignore': {'sha256': 'c31e9339369825805dd0766b6b7d07e7b5b6ce9f5d0b87a35b8fef01d0d8e841', 'bytes': 51, 'executable': False}, 'AUTHORS': {'sha256': '0f5d7d97de020316971dd61c12e2b2f758a83919f7efa4b35c589b39e8de6af2', 'bytes': 1182, 'executable': False}, 'ChangeLog': {'sha256': '1346742f91566a125efc2d30cee94fe945d328468f5985cbcac77f9d724382f3', 'bytes': 6802, 'executable': False}, 'LICENSE': {'sha256': '8bc2ebd0f1c1d1f1691555d2665a4f9d8865d659637926dfaf90bdedb41cd802', 'bytes': 1492, 'executable': False}, 'Makefile.in': {'sha256': 'ef1773cc87f98381d94d4d180851af540950ac5a30ae160fdcc31534b8b31de9', 'bytes': 730, 'executable': False}, 'README': {'sha256': '586eea52c0d2709157d4ff623477fb101d620c493edaa916c288059449f814a7', 'bytes': 2624, 'executable': False}, 'configure': {'sha256': 'e52956911193d03199bdb6ca072450ada8153d9a9fb9244ee7ba2b36ff1d62fd', 'bytes': 144744, 'executable': True}, 'configure.ac': {'sha256': '2b41e4cf75641bb78e2f8cc6ec8ac644f1a9b48361fa7bf62bf6f235d58b6d27', 'bytes': 1136, 'executable': False}, 'main.c': {'sha256': 'da8778126e65557bdada9e72565c03237e615965d9f4a8f58bde2883d14fe23a', 'bytes': 8236, 'executable': False}, 'main.h': {'sha256': '46a34d6012f2451997a94ef4bb669290c5ab22c4d41aa2836239c4cdeaae67a0', 'bytes': 1005, 'executable': False}, 'pdf.c': {'sha256': 'a1f5b40644bf2e2ff3156e1760f96694d95d634f37b7f23481b6e1bee512dcfe', 'bytes': 33255, 'executable': False}, 'pdf.h': {'sha256': 'd7dca1a469ac2aa27642be067b5ae5a0fc92ddcbaa20f584eb964c776d679811', 'bytes': 2646, 'executable': False}, 'pdfresurrect.1': {'sha256': 'd1299f16aeb89f13bff32d0279de0c41354cd858a238a8059c4a84ad3e67c7bc', 'bytes': 2941, 'executable': False}}
assert len(original)==13 and not Path('.packaging-qa').exists() and not Path('.packaging-originals').exists()
notices=Path('.packaging-originals/source-notices');notices.mkdir(parents=True)
for name,row in original.items():
    p=Path(name);b=p.read_bytes()
    assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],name
    assert bool(p.stat().st_mode&0o111)==row['executable'],name
    q=notices/(name+'.notice');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
Path('.packaging-originals/source.json').write_text(json.dumps(original,sort_keys=True)+'\n')
(notices/'SHA256SUMS').write_text(''.join(row['sha256']+'  '+name+'.notice\n' for name,row in sorted(original.items())))
Path('.packaging-qa').mkdir()
PY_ORIGINALS
# Preserve all 13 original notices before applying the one pinned source patch.
sha256sum -c <<'EOF_PATCH_SHA'
0019baf693ce147e7ba9af598548e30fe75ffdf329bb3965dd56fdffb83f13c9  %{PATCH0}
EOF_PATCH_SHA
patch --batch --forward --fuzz=0 -p1 < %{PATCH0}
python3 - <<'PY_POSTPATCH'
import hashlib,json
from pathlib import Path
original=json.loads(Path('.packaging-originals/source.json').read_text());assert len(original)==13
post={'configure.ac': {'sha256': '7e52e65eaadeaeffa3bc4562a836b460a8ab7ab46d5f34c5f02b8c8b2a3db0f6', 'bytes': 1141, 'executable': False}, 'configure': {'sha256': '43090de5ab38f9d965e98f9108e4c08fe1fb0caaf246a98ee3b88feda9624617', 'bytes': 144749, 'executable': True}}
assert set(post)=={'configure','configure.ac'}
for name,row in original.items():
    p=Path(name);b=p.read_bytes();expected=post.get(name,row)
    assert p.is_file() and not p.is_symlink() and len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256'] and bool(p.stat().st_mode&0o111)==row['executable'],name
    notice=Path('.packaging-originals/source-notices',name+'.notice');original_bytes=notice.read_bytes()
    assert notice.is_file() and not notice.is_symlink() and len(original_bytes)==row['bytes'] and hashlib.sha256(original_bytes).hexdigest()==row['sha256'],name
print('PDFRESURRECT_SOURCE_PATCH_PROOF '+json.dumps(dict(phase='prep',original_files=13,unchanged_original_files=11,postpatch_files=post,all_13_original_notice_bytes_unchanged=True,patch_sha256='0019baf693ce147e7ba9af598548e30fe75ffdf329bb3965dd56fdffb83f13c9'),sort_keys=True))
PY_POSTPATCH
cat > .packaging-qa/run-qa.py <<'EOF_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
"""Owned deterministic classic-PDF fixtures, not a general PDF/security oracle.
--data-only proves byte offsets without invoking pdfresurrect or creating files.
All program invocations are reserved for the locked target build/install CI.
"""
import argparse,base64,hashlib,json,os,re,stat,struct,subprocess,tempfile
from pathlib import Path

def sha(data):return hashlib.sha256(data).hexdigest()
def fixture(*,creator='Alpha',title='Title-A',indirect=False,incremental=False):
 data=bytearray(b'%%PDF-1.4\n%%'+b'Q'*1100+b'\n');offsets={}
 fields={'Title':'('+title+')','Creator':'('+creator+')'}
 objects={1:b'<< /Type /Catalog /Pages 2 0 R >>',2:b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',3:b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>'}
 objects[4]=('<< /Title '+('5 0 R' if indirect else fields['Title'])+' /Creator '+fields['Creator']+' >>').encode()
 if indirect:objects[5]=fields['Title'].encode()
 for number,value in sorted(objects.items()):
  offsets[number]=len(data);data.extend(f'{number} 0 obj\n'.encode()+value+b'\nendobj\n')
 versions=[]
 def crossref(values,previous=None):
  xref=len(data);size=max(values)+1;data.extend(f'xref\n0 {size}\n'.encode()+b'0000000000 65535 f \n')
  for number in range(1,size):data.extend(f'{values[number]:010d} 00000 n \n'.encode())
  trailer=f'trailer\n<< /Size {size} /Root 1 0 R /Info 4 0 R'+(' /Prev '+str(previous) if previous is not None else '')+' >>\n'
  data.extend(trailer.encode()+f'startxref\n{xref}\n%%%%EOF\n'.encode());versions.append(dict(version=len(versions)+1,xref=xref,size=size,object_offsets=dict(values),EOF_end=len(data)))
 crossref(offsets)
 if incremental:
  previous=versions[-1]['xref'];offsets[4]=len(data);data.extend(b'4 0 obj\n<< /Title (Revision-B) /Creator (Second) >>\nendobj\n');crossref(offsets,previous)
 return bytes(data),versions

def prove(data,versions):
 assert data.startswith(b'%%PDF-1.4\n') and len(data)>=1023
 parsed=list(re.finditer(rb'startxref\n([0-9]+)\n%%%%EOF\n',data));assert len(parsed)==len(versions)
 for match,version in zip(parsed,versions):
  x=version['xref'];assert int(match[1])==x and data[x:].startswith(b'xref\n') and match.end()==version['EOF_end']
  lines=data[x:match.start()].splitlines();assert lines[1]==f"0 {version['size']}".encode() and lines[2]==b'0000000000 65535 f '
  for number in range(1,version['size']):
   row=lines[2+number];assert len(row)==19 and row[17:]==b'n ' and int(row[:10])==version['object_offsets'][number] and data[int(row[:10]):].startswith(f'{number} 0 obj\n'.encode())
  assert f"/Size {version['size']} /Root 1 0 R /Info 4 0 R".encode() in data[x:match.start()]
 return dict(bytes=len(data),sha256=sha(data),versions=versions,EOF_markers=len(parsed),classic_uncompressed_xrefs=True,rendering_security_or_all_PDF_features_not_claimed=True)

def summary(name,versions):
 rows=[];types={0:'Catalog',1:'Catalog',2:'Pages',3:'Page',4:'Unknown',5:'Unknown'}
 if len(versions)==1:rows.append(f'{name}: There is only one version of this PDF\n')
 for i,version in enumerate(versions):
  for number in range(version['size']):
   status='A' if i==0 else ('D' if number==0 else ('M' if version['object_offsets'][number]!=versions[i-1]['object_offsets'].get(number) else '?'))
   rows.append(f"{name}: --{status}-- Version {i+1} -- Object {number} ({types[number]})\n")
 rows.append(f'---------- {name} ----------\nVersions: {len(versions)}\n')
 for i,version in enumerate(versions):rows.append(f"Version {i+1} -- {version['size']} objects\n")
 return ''.join(rows).encode()

def creator_output(name,title,creator):
 result=f'{name}: 1\nPDF Version: 1.4\n'
 for key in ['Title','Author','Subject','Keywords','Creator','Producer','CreationDate','ModDate','Trapped']:
  result+=key+': '+({'Title':'('+title+')','Creator':'('+creator+')'}.get(key,''))+'\n'
 return (result+'\n').encode()

def models():
 one,ov=fixture();two,tv=fixture(creator='First',title='Revision-A',incremental=True);inline,iv=fixture(creator='Alpha',title='Title-A');indirect,jv=fixture(creator='Beta',title='Delta',indirect=True)
 rows={'one.pdf':(one,ov),'two.pdf':(two,tv),'inline.pdf':(inline,iv),'indirect.pdf':(indirect,jv),'extract.pdf':(two,tv)}
 proof={name:prove(data,versions) for name,(data,versions) in rows.items()};invalid=b'Not a PDF document\n'+b'X'*1100;assert len(invalid)>=1023 and b'%%PDF-' not in invalid
 proof['invalid.pdf']=dict(bytes=len(invalid),sha256=sha(invalid),deliberate_non_PDF=True)
 return rows,invalid,proof

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--program');ap.add_argument('--required-program');ap.add_argument('--data-only',action='store_true');a=ap.parse_args();rows,invalid,data_proof=models()
 if a.data_only:
  print(json.dumps(dict(data_only=True,fixtures=data_proof,groups=6,planned_CLI_invocations=10,program_invocations=0,files_written=0),sort_keys=True));return
 assert a.program and not Path(a.program).is_symlink();program=Path(a.program).resolve(strict=True);selfpath=Path(__file__).resolve(strict=True)
 if a.required_program:assert os.path.samefile(program,Path(a.required_program).resolve(strict=True))
 raw=program.read_bytes();assert raw[:6]==b'\x7fELF\x02\x01' and struct.unpack_from('<H',raw,18)[0]==243 and struct.unpack_from('<H',raw,16)[0] in {2,3}
 before_program=sha(raw);before_self=sha(selfpath.read_bytes());identity=program.stat();work=Path(tempfile.mkdtemp(prefix='pdfresurrect-qa-'));logs=work/'raw';logs.mkdir();records=[];env=dict(os.environ);env.update(LC_ALL='C',LANG='C',TZ='UTC')
 for key in ['LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH','PYTHONHOME']:env.pop(key,None)
 def raw_record(label,argv,cwd,stdout,stderr,code,timeout=False):
  for suffix,data in [('stdout',stdout),('stderr',stderr)]:(logs/(label+'.'+suffix)).open('xb').write(data)
  row=dict(label=label,argv=argv,cwd=str(cwd),environment={k:env.get(k) for k in ['LC_ALL','LANG','TZ','LD_PRELOAD','LD_LIBRARY_PATH']},exit=code,timeout=timeout,stdout_sha256=sha(stdout),stdout_base64=base64.b64encode(stdout).decode(),stderr_sha256=sha(stderr),stderr_base64=base64.b64encode(stderr).decode());records.append(row);print(json.dumps(row,sort_keys=True),flush=True);return row
 def invoke(label,args,cwd,want_stdout,want_stderr=b'',want_exit=0):
  argv=[str(program)]+args
  try:r=subprocess.run(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=20);row=raw_record(label,argv,cwd,r.stdout,r.stderr,r.returncode)
  except subprocess.TimeoutExpired as ex:
   raw_record(label,argv,cwd,ex.stdout or b'',ex.stderr or b'',None,True);raise AssertionError('CLI timeout is failure, not success') from ex
  assert row['exit']==want_exit and r.stdout==want_stdout and r.stderr==want_stderr,(label,'exact status/stdout/stderr mismatch')
 def put(folder,name):
  d,v=rows[name];p=folder/name;p.open('xb').write(d);p.chmod(0o644);return p,v
 try:
  for label,args in [('ELF-header',['readelf','-h',str(program)]),('build-ID',['readelf','-n',str(program)])]:
   r=subprocess.run(args,cwd=work,env=env,capture_output=True,timeout=20);raw_record(label,args,work,r.stdout,r.stderr,r.returncode);assert r.returncode==0 and r.stderr==b''
   if label=='build-ID':assert re.search(rb'Build ID: [0-9a-f]+',r.stdout)
  usage=b'-- pdfresurrect v0.23 --\nUsage: ./pdfresurrect <file.pdf> [-i] [-w] [-q]\n\t -i Display PDF creator information\n\t -w Write the PDF versions and summary to disk\n\t -q Display only the number of versions contained in the PDF\n'
  invoke('01-usage-version',[],work,usage)
  p,v=put(work,'one.pdf');invoke('02-one-version',[p.name],work,summary(p.name,v));assert sha(p.read_bytes())==data_proof[p.name]['sha256']
  p,v=put(work,'two.pdf');invoke('03-two-versions',[p.name],work,summary(p.name,v));invoke('04-quiet-count',[p.name,'-q'],work,b'two.pdf: 2\n');assert sha(p.read_bytes())==data_proof[p.name]['sha256']
  p,v=put(work,'inline.pdf');invoke('05-inline-creator',[p.name,'-q','-i'],work,creator_output(p.name,'Title-A','Alpha'))
  p,v=put(work,'indirect.pdf');invoke('06-indirect-title',[p.name,'-q','-i'],work,creator_output(p.name,'Delta','Beta'))
  extract=work/'extraction';extract.mkdir();p,v=put(extract,'extract.pdf');original=p.read_bytes();invoke('07-extract-both',[p.name,'-w'],extract,b'');directory=extract/'extract-versions';assert {x.name for x in directory.iterdir()}=={'extract-version-1.pdf','extract-version-2.pdf','extract-versions.summary'}
  extracted={}
  for version in v:
   output=directory/f"extract-version-{version['version']}.pdf";expected=original+f"\r\nstartxref\r\n{version['xref']}\r\n%%%%EOF".encode();actual=output.read_bytes();assert actual==expected and actual[:len(original)]==original and actual[version['xref']:].startswith(b'xref\n');extracted[output.name]=dict(bytes=len(actual),sha256=sha(actual),selected_xref=version['xref'],full_original_prefix_retained=True)
  assert (directory/'extract-versions.summary').read_bytes()==summary('extract.pdf',v);state={x.name:sha(x.read_bytes()) for x in directory.iterdir()};assert p.read_bytes()==original
  invoke('08-existing-directory',[p.name,'-w'],extract,b'',b'[pdfresurrect] -- Error -- This directory already exists, PDF version extraction will not occur.\n',255);assert state=={x.name:sha(x.read_bytes()) for x in directory.iterdir()} and p.read_bytes()==original
  invalid_path=work/'invalid.pdf';invalid_path.open('xb').write(invalid);invoke('09-invalid-input',[invalid_path.name],work,b'',b"[pdfresurrect] -- Error -- 'invalid.pdf' specified is not a valid PDF\n",255)
  assert not (work/'missing.pdf').exists();invoke('10-missing-input',['missing.pdf'],work,b'',b"[pdfresurrect] -- Error -- Could not open file 'missing.pdf'\n",255)
  assert len([r for r in records if r['argv'][0]==str(program)])==10 and program.stat().st_ino==identity.st_ino and program.stat().st_dev==identity.st_dev and sha(program.read_bytes())==before_program and sha(selfpath.read_bytes())==before_self
  for name,(data,_) in rows.items():
   path=(extract/name) if name=='extract.pdf' else work/name;assert path.read_bytes()==data
  result=dict(status='passed',program=str(program),program_sha256_before=before_program,program_sha256_after=sha(program.read_bytes()),program_same_file_before_after=True,required_program_samefile=bool(a.required_program),helper=str(selfpath),helper_sha256_before=before_self,helper_sha256_after=sha(selfpath.read_bytes()),work=str(work),ELF_class=64,ELF_machine=243,build_ID_observed=True,semantic_groups=6,CLI_invocations=10,metadata_readelf_invocations=2,all_CLI_status_stdout_stderr_exact=True,data_fixtures=data_proof,extracted_versions=extracted,original_input_bytes_unchanged=True,extraction_not_scrubbing=True,all_PDFs_or_security_or_performance_not_claimed=True,commands=records)
  (work/'qa-result.json').open('x').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True),flush=True)
 except BaseException as ex:
  (work/'qa-failure.json').open('x').write(json.dumps(dict(error=repr(ex),work=str(work),program=str(program),program_sha256_before=before_program,helper_sha256_before=before_self,data_fixtures=data_proof,commands=records),indent=2)+'\n');raise

if __name__=='__main__':main()
EOF_QA
chmod 0755 .packaging-qa/run-qa.py
sha256sum -c <<'EOF_QA_SHA'
5358f476e15a3c51ccd4a2d261258dfcc5bb3ecbea25ad9f01338165d3859d75  .packaging-qa/run-qa.py
cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  %{SOURCE1}
EOF_QA_SHA

%build
python3 - <<'PY_SOURCE_BEFORE_BUILD'
import hashlib,json
from pathlib import Path
original=json.loads(Path('.packaging-originals/source.json').read_text());assert len(original)==13
post={'configure.ac': {'sha256': '7e52e65eaadeaeffa3bc4562a836b460a8ab7ab46d5f34c5f02b8c8b2a3db0f6', 'bytes': 1141, 'executable': False}, 'configure': {'sha256': '43090de5ab38f9d965e98f9108e4c08fe1fb0caaf246a98ee3b88feda9624617', 'bytes': 144749, 'executable': True}}
assert set(post)=={'configure','configure.ac'}
for name,row in original.items():
    p=Path(name);b=p.read_bytes();expected=post.get(name,row)
    assert p.is_file() and not p.is_symlink() and len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256'] and bool(p.stat().st_mode&0o111)==row['executable'],name
    notice=Path('.packaging-originals/source-notices',name+'.notice');original_bytes=notice.read_bytes()
    assert notice.is_file() and not notice.is_symlink() and len(original_bytes)==row['bytes'] and hashlib.sha256(original_bytes).hexdigest()==row['sha256'],name
print('PDFRESURRECT_SOURCE_PATCH_PROOF '+json.dumps(dict(phase='build',original_files=13,unchanged_original_files=11,postpatch_files=post,all_13_original_notice_bytes_unchanged=True,patch_sha256='0019baf693ce147e7ba9af598548e30fe75ffdf329bb3965dd56fdffb83f13c9'),sort_keys=True))
PY_SOURCE_BEFORE_BUILD
# Keep the original effective -O3 -Wall as well as the target RPM flags.
export CFLAGS="%{optflags} -O3 -Wall"
export LDFLAGS="%{?build_ldflags} -Wl,--build-id"
# Checked-in configure uses Bash += syntax. No autoreconf or helper replacement.
# Preserve the original configure argv and exit status; diagnostics are not a fix.
if /bin/bash ./configure --prefix=%{_prefix} --bindir=%{_bindir} --mandir=%{_mandir}; then
    :
else
    configure_status=$?
    printf 'PDFRESURRECT_CONFIG_LOG_BEGIN status=%%s\n' "$configure_status"
    if test -f config.log && test ! -L config.log; then
        if cat -- config.log; then :; else printf 'PDFRESURRECT_CONFIG_LOG_READ_FAILED\n'; fi
    else
        printf 'PDFRESURRECT_CONFIG_LOG_MISSING_OR_SYMLINK\n'
    fi
    printf 'PDFRESURRECT_CONFIG_LOG_END status=%%s\n' "$configure_status"
    exit "$configure_status"
fi
make %{?_smp_mflags}
test -x pdfresurrect
! grep -E -- '(^|[[:space:]])-DPDFRESURRECT_EXPERIMENTAL([=[:space:]]|$)' Makefile

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_datadir}/pdfresurrect-tests
install -m0644 .packaging-qa/run-qa.py %{buildroot}%{_datadir}/pdfresurrect-tests/
(cd %{buildroot}%{_datadir}/pdfresurrect-tests && sha256sum run-qa.py > SHA256SUMS)
install -d %{buildroot}%{_licensedir}/%{name}/source-notices
cp -a .packaging-originals/source-notices/. %{buildroot}%{_licensedir}/%{name}/source-notices/
install -m0644 LICENSE AUTHORS %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/
install -d %{buildroot}%{_docdir}/%{name}
install -m0644 README ChangeLog %{buildroot}%{_docdir}/%{name}/

%check
export LC_ALL=C LANG=C
python3 - <<'PY_SOURCE_AFTER'
import hashlib,json
from pathlib import Path
original=json.loads(Path('.packaging-originals/source.json').read_text());assert len(original)==13
post={'configure.ac': {'sha256': '7e52e65eaadeaeffa3bc4562a836b460a8ab7ab46d5f34c5f02b8c8b2a3db0f6', 'bytes': 1141, 'executable': False}, 'configure': {'sha256': '43090de5ab38f9d965e98f9108e4c08fe1fb0caaf246a98ee3b88feda9624617', 'bytes': 144749, 'executable': True}}
assert set(post)=={'configure','configure.ac'}
for name,row in original.items():
    p=Path(name);b=p.read_bytes();expected=post.get(name,row)
    assert p.is_file() and not p.is_symlink() and len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256'] and bool(p.stat().st_mode&0o111)==row['executable'],name
    notice=Path('.packaging-originals/source-notices',name+'.notice');original_bytes=notice.read_bytes()
    assert notice.is_file() and not notice.is_symlink() and len(original_bytes)==row['bytes'] and hashlib.sha256(original_bytes).hexdigest()==row['sha256'],name
print('PDFRESURRECT_SOURCE_PATCH_PROOF '+json.dumps(dict(phase='check',original_files=13,unchanged_original_files=11,postpatch_files=post,all_13_original_notice_bytes_unchanged=True,patch_sha256='0019baf693ce147e7ba9af598548e30fe75ffdf329bb3965dd56fdffb83f13c9'),sort_keys=True))
PY_SOURCE_AFTER
sha256sum -c <<'EOF_CHECK_SHA'
5358f476e15a3c51ccd4a2d261258dfcc5bb3ecbea25ad9f01338165d3859d75  .packaging-qa/run-qa.py
EOF_CHECK_SHA
python3 .packaging-qa/run-qa.py --data-only
python3 .packaging-qa/run-qa.py --program "$PWD/pdfresurrect"

%files
%license %{_licensedir}/%{name}
%doc %{_docdir}/%{name}
%{_bindir}/pdfresurrect
%{_mandir}/man1/pdfresurrect.1*
%dir %{_datadir}/pdfresurrect-tests
%{_datadir}/pdfresurrect-tests/run-qa.py
%{_datadir}/pdfresurrect-tests/SHA256SUMS

%changelog
* Wed Oct 28 2026 openEuler RISC-V package contributors - 0.23-1
- Preserve incoming compiler hardening flags in both configure inputs.
- Preserve original binary/manual defaults, all notices and strict QA.
- Add bounded classic-PDF revision checks without enabling experimental scrub.
