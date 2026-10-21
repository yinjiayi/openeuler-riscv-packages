# SPDX-License-Identifier: MIT
Name:           jshon
Version:        20131105
Release:        1%{?dist}
Summary:        JSON parser and manipulator for shell pipelines
License:        MIT
URL:            https://github.com/keenerd/jshon
Source0:        jshon-20131105.tar.gz
Patch0:         patches/0001-terminate-and-check-input.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3
BuildRequires:  pkgconfig
BuildRequires:  jansson-devel

%description
Read, query and manipulate JSON with the original shell-oriented stack API.

%package tests
Summary:        Offline functional and input regression checks for jshon
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Original fixed stable source, notice and downstream command checks. The upstream
release has no declared test/check target; no original tests are removed.

%prep
%setup -q
%patch0 -p1
cat > downstream-qa.py <<'JSHON_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi; distributed with the original retained MIT notice.
"""Downstream functional/regression checks; no upstream test target is declared."""
import gzip,hashlib,json,os,subprocess,sys,tarfile,tempfile
from pathlib import Path
root=Path(sys.argv[1]).resolve();binary=root/'usr/bin/jshon';checks=[]
archive=root/'usr/share/jshon/qa/jshon-20131105.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='28420f6f02c6b762732898692cc0b0795cfe1a59fbfb24e67b80f332cf6d4fa2'
with tarfile.open(archive,'r:gz')as tf:
 notice=tf.extractfile('jshon-20131105/LICENSE').read()
 for name in ('jshon','jshon-tests'):assert(root/'usr/share/licenses'/name/'LICENSE').read_bytes()==notice
 man=root/'usr/share/man/man1/jshon.1.gz'
 actual=gzip.decompress(man.read_bytes())if man.exists()else man.with_suffix('').read_bytes()
 assert actual==tf.extractfile('jshon-20131105/jshon.1').read()
checks.append('fixed-original-archive-manual-license')
env=dict(os.environ,LC_ALL='C',MALLOC_PERTURB_='165')
def run(args,data=b'',status=0,quiet=True,stderr=None):
 p=subprocess.run([str(binary),*args],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15,env=env)
 assert p.returncode==status,(args,p.returncode,p.stdout,p.stderr)
 if stderr is not None:assert p.stderr==stderr,(args,p.stderr,stderr)
 elif quiet:assert not p.stderr,(args,p.stderr)
 return p.stdout
def plain(name,args,data,expected,status=0,quiet=True,stderr=None):
 assert run(args,data,status,quiet,stderr)==expected,name;checks.append(name)
def js(name,args,data,expected):
 assert json.loads(run(args,data))==expected,name;checks.append(name)
sample=b'{"a":1,"b":[true,false,null,"str"],"c":{"d":4,"e":5}}'
plain('honest-original-version',['--version'],b'','20131105\n'.encode())
plain('type',['-t'],sample,b'object\n')
plain('length',['-l'],sample,b'3\n')
plain('keys',['-k'],sample,b'a\nb\nc\n')
js('extract-object',['-e','c'],sample,{'d':4,'e':5})
plain('across-types',['-e','b','-a','-t'],sample,b'bool\nbool\nnull\nstring\n')
plain('unstring',['-e','b','-e','3','-u'],sample,b'str\n')
plain('negative-extract',['-e','b','-e','-1','-u'],sample,b'str\n')
plain('history-pop',['-e','c','-e','d','-u','-p','-e','e','-u'],sample,b'4\n5\n')
js('delete-key',['-d','b'],sample,{'a':1,'c':{'d':4,'e':5}})
js('insert-string',['-s','one','-i','a'],sample,{'a':'one','b':[True,False,None,'str'],'c':{'d':4,'e':5}})
js('insert-array-append',['-e','b','-n','7','-i','append'],sample,[True,False,None,'str',7])
js('by-reference-original',['-e','c','-n','7','-i','d','-p'],sample,{'a':1,'b':[True,False,None,'str'],'c':{'d':7,'e':5}})
js('by-value-original',['-V','-e','c','-n','7','-i','d','-p'],sample,{'a':1,'b':[True,False,None,'str'],'c':{'d':4,'e':5}})
js('jsonp',['-P'],b'callback('+sample+b');',json.loads(sample))
plain('sorted-keys',['-S','-k'],b'{"z":0,"a":1}',b'a\nz\n')
plain('nul-delimiter',['-0','-e','b','-e','3','-u'],sample,b'str\0')
js('json-literal',['-e','c','-j'],sample,{'d':4,'e':5})
js('utf8',['-Q','-s','RISC-V 中文'],b'', 'RISC-V 中文')
js('empty-pipe-creation-regression',['-Q','-n','object','-n','array','-i','data'],b'',{'data':[]})
plain('empty-pipe-json-regression',['-Q'],b'',b'')
plain('empty-jsonp-regression',['-Q','-P'],b'',b'')
plain('invalid-json',['-Q'],b'{',b'',1)
plain('missing-key',['-Q','-e','absent'],sample,b'',1)
plain('invalid-option',['-Q','-?'],sample,b'',2,stderr=os.fsencode(binary)+b": invalid option -- '?'\n")
with tempfile.TemporaryDirectory(prefix='jshon-qa-')as tmp:
 file=Path(tmp)/'data.json';file.write_bytes(sample)
 js('regular-file-termination-regression',['-F',str(file)],b'',json.loads(sample))
 plain('in-place',['-I','-F',str(file),'-s','one','-i','a'],b'',b'')
 assert json.loads(file.read_bytes())['a']=='one'
 file.write_bytes(b'');plain('empty-file',['-Q','-F',str(file)],b'',b'')
 plain('missing-file-regression',['-Q','-F',str(Path(tmp)/'missing')],b'',b'',1,False)
 js('multi-buffer-stream',[],json.dumps({'text':'x'*50000}).encode(),{'text':'x'*50000})
print('JSHON_QA_OK',len(checks),','.join(checks))
JSHON_QA

%build
# Environment flags are extended by the original Makefile, including -Werror.
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build

%install
%make_install
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/jshon
%{_mandir}/man1/jshon.1*

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 20131105-1
- Retain stable defaults and compiler warnings, repair input handling, add checks.
