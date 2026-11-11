# SPDX-License-Identifier: Apache-2.0
Name:           libtree
Version:        3.1.1
Release:        1%{?dist}
Summary:        Explain ELF shared-library dependency trees
License:        MIT AND Apache-2.0
URL:            https://github.com/haampie/libtree
Source0:        libtree-v3.1.1.tar.gz
Source1:        Apache-2.0.txt
Patch0:         0001-parameterize-inert-ELF-class-fixtures.patch
Patch1:         0002-advance-long-dependencies-and-bound-paths.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
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
Requires:       diffutils
Requires:       findutils
Requires:       grep
Requires:       python3

%description
Libtree reads ELF files and prints their shared-library dependencies, including
RPATH, RUNPATH and environment search provenance. It does not execute inspected
ELF files. Preserve the original CLI, install target and all nine test suites.
The ELF32 test data is not a 32-bit runtime or installed package. The package
itself remains riscv64/RVA23; no complete native-loader or security claim is made.

%prep
%setup -q -n haampie-libtree-1521dfe
find . -type f -print | LC_ALL=C sort > ../libtree-original-files.list
test "$(wc -l < ../libtree-original-files.list)" -eq 24
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    destination="source-notices/$rel.notice"
    install -d "${destination%/*}"
    cp -p "$item" "$destination"
    chmod 0644 "$destination"
done < ../libtree-original-files.list
(cd source-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../libtree-original-SHA256SUMS
mv ../libtree-original-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 24
%autopatch -p1
cp -p %{SOURCE1} Apache-2.0.txt
cat > regressions.py <<'LIBTREE_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler package contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Six additive CLI groups. Only libtree runs: generated ELF files are data.
This is NOT a replacement for any of the nine upstream compiler-fixture suites.
"""
from pathlib import Path
import base64,hashlib,json,os,shutil,struct,subprocess,sys,tempfile

def elf(bits=64,machine=243,needed=(),soname=None,rpath=None,runpath=None):
    ident=b'\x7fELF'+bytes([1 if bits==32 else 2,1,1])+b'\0'*9
    eh=52 if bits==32 else 64;ph=32 if bits==32 else 56
    strings=bytearray(b'\0');entries=[]
    for tag,value in [(14,soname),(15,rpath),(29,runpath)]+[(1,v) for v in needed]:
        if value is None:continue
        entries.append((tag,len(strings)));strings.extend(value.encode()+b'\0')
    # The virtual load address is0x1000, string-table file offset0x400.
    entries=[(5,0x1400)]+entries+[(0,0)]
    dyn=b''.join(struct.pack('<iI' if bits==32 else '<qQ',a,b) for a,b in entries)
    assert len(dyn)<=0x300
    size=0x400+len(strings)
    if bits==32:
        header=ident+struct.pack('<HHIIIIIHHHHHH',3,machine,1,0,eh,0,0,eh,ph,2,0,0,0)
        load=struct.pack('<IIIIIIII',1,0,0x1000,0x1000,size,size,4,0x1000)
        dynamic=struct.pack('<IIIIIIII',2,0x100,0x1100,0x1100,len(dyn),len(dyn),4,4)
    else:
        header=ident+struct.pack('<HHIQQQIHHHHHH',3,machine,1,0,eh,0,0,eh,ph,2,0,0,0)
        load=struct.pack('<IIQQQQQQ',1,4,0,0x1000,0x1000,size,size,0x1000)
        dynamic=struct.pack('<IIQQQQQQ',2,4,0x100,0x1100,0x1100,len(dyn),len(dyn),8)
    assert len(header)==eh and len(load)==ph and len(dynamic)==ph
    data=bytearray(size);data[:eh]=header;data[eh:eh+ph]=load;data[eh+ph:eh+2*ph]=dynamic;data[0x100:0x100+len(dyn)]=dyn;data[0x400:]=strings
    return bytes(data)

def main():
    assert len(sys.argv)==2;program=Path(sys.argv[1]).resolve(strict=True);work=Path(tempfile.mkdtemp(prefix='libtree-cli-qa-'));evidence=[];files=[]
    helper=Path(__file__).resolve(strict=True);program_before=hashlib.sha256(program.read_bytes()).hexdigest();helper_before=hashlib.sha256(helper.read_bytes()).hexdigest()
    env=dict(os.environ);env.pop('LD_LIBRARY_PATH',None);env.pop('LD_PRELOAD',None);env.update(LC_ALL='C',LANG='C',NO_COLOR='1')
    def put(path,data):
        path=work/path;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);path.chmod(0o444);files.append(path);return path
    def invoke(label,args,code=0,stdout=None,stderr=b'',extra=None,cwd=None):
        current=dict(env);current.update(extra or {})
        try:
            result=subprocess.run([str(program),'--ldconf','/dev/null']+list(map(str,args)),cwd=cwd or work,env=current,stdin=subprocess.DEVNULL,capture_output=True,timeout=10,check=False)
            out,err,status=result.stdout,result.stderr,result.returncode
        except subprocess.TimeoutExpired as failure:
            out,err,status=failure.stdout or b'',failure.stderr or b'',124
        evidence.append(dict(label=label,argv=[str(program),'--ldconf','/dev/null']+list(map(str,args)),cwd=str(cwd or work),environment={k:current.get(k) for k in ['LC_ALL','LANG','NO_COLOR','LD_LIBRARY_PATH','LD_PRELOAD']},program_realpath=str(program),program_sha256=hashlib.sha256(program.read_bytes()).hexdigest(),helper_realpath=str(helper),helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),exit=status,stdout_sha256=hashlib.sha256(out).hexdigest(),stdout_base64=base64.b64encode(out).decode(),stderr_sha256=hashlib.sha256(err).hexdigest(),stderr_base64=base64.b64encode(err).decode()))
        assert status==code,(label,status,code);assert stderr is None or err==stderr,(label,err,stderr);assert stdout is None or out==stdout,(label,out,stdout);return out
    def tree(root,child=None,reason='rpath'):
        return (str(root)+' \n'+('└── '+str(child)+' ['+reason+']\n' if child is not None else '')).encode()
    def missing(root,name):
        indent='    ┊'
        lines=[str(root)+' ', '└── '+name+' not found', indent+' Paths considered in this order:', indent+' 1. rpath:', indent+'    depth 1', indent+'    '+str(root.parent)+'/search', indent+' 2. LD_LIBRARY_PATH was not set', indent+' 3. runpath was not set', indent+' 4. ld config files:', indent+' 5. Standard paths:']
        lines += [indent+'    '+p for p in ['/lib','/lib64','/usr/lib','/usr/lib64']]
        return ('\n'.join(lines)+'\n').encode()
    try:
        invoke('version',['--version'],stdout=b'3.1.1\n');print('ok 1 - version')
        invalid=put(Path('invalid.elf'),b'not-an-ELF');invoke('invalid-magic',[invalid],code=11,stdout=b'',stderr=('Error ['+str(invalid)+']: Invalid ELF magic bytes\n').encode())
        invalid_class=put(Path('invalid-class.elf'),b'\x7fELF'+bytes([0,1,1])+b'\0'*9);invoke('invalid-class',[invalid_class],code=12,stdout=b'',stderr=('Error ['+str(invalid_class)+']: Invalid ELF class\n').encode());print('ok 2 - precise malformed input errors')
        for bits in [32,64]:
            plain=put(Path('plain'+str(bits)+'.elf'),elf(bits=bits));invoke('plain-'+str(bits),[plain],stdout=tree(plain))
        print('ok 3 - ELF32 and ELF64 data')
        for kind in ['class','machine']:
            base=Path(kind);wrong=put(base/'wrong/libfixture.so',elf(bits=32 if kind=='class' else 64,machine=243 if kind=='class' else 62,soname='libfixture.so'));right=put(base/'right/libfixture.so',elf(soname='libfixture.so'));root=put(base/'root.elf',elf(needed=['libfixture.so'],rpath='$ORIGIN/wrong:$ORIGIN/right'))
            invoke('compatible-'+kind,['-p',root],stdout=tree(root,right))
        print('ok 4 - dependency class and machine compatibility')
        base=Path('precedence');r=put(base/'rpath/libfixture.so',elf(soname='libfixture.so'));v=put(base/'env/libfixture.so',elf(soname='libfixture.so'));put(base/'runpath/libfixture.so',elf(soname='libfixture.so'))
        root_r=put(base/'root-rpath.elf',elf(needed=['libfixture.so'],rpath='$ORIGIN/rpath'));root_u=put(base/'root-runpath.elf',elf(needed=['libfixture.so'],runpath='$ORIGIN/runpath'))
        invoke('rpath-before-environment',['-p',root_r],stdout=tree(root_r,r),extra={'LD_LIBRARY_PATH':str(v.parent)})
        invoke('environment-before-runpath',['-p',root_u],stdout=tree(root_u,v,'LD_LIBRARY_PATH'),extra={'LD_LIBRARY_PATH':str(v.parent)});print('ok 5 - original RPATH environment RUNPATH order')
        for kind,name in [('absolute','/'+'x'*4096),('soname','x'*4096)]:
            root=put(Path('long-'+kind+'.elf'),elf(needed=[name],rpath='$ORIGIN/search'))
            invoke('long-'+kind,[root],code=28,stdout=missing(root,name),stderr=('Error ['+str(root)+']: Not all dependencies were found\n').encode())
        # Exactly4096 chars fill the old path buffer; its suffix must not be
        # reinterpreted as a new relative directory in the current working dir.
        put(Path('victim/libfixture.so'),elf(soname='libfixture.so'));right=put(Path('long-search/right/libfixture.so'),elf(soname='libfixture.so'))
        root=put(Path('long-search/root.elf'),elf(needed=['libfixture.so'],rpath='/'+'z'*4095+'victim:$ORIGIN/right'))
        invoke('long-search-component',['-p',root],stdout=tree(root,right));print('ok 6 - bounded long-needed and search-component regressions')
        assert len(evidence)==12 and len(files)==20
        assert hashlib.sha256(program.read_bytes()).hexdigest()==program_before and hashlib.sha256(helper.read_bytes()).hexdigest()==helper_before
        print('libtree-cli: 6 groups passed')
    finally:
        # All command streams and every generated data byte survive in CI logs
        # on either success or failure; the files are never executed or installed.
        print('LIBTREE-OWNED-BINDING '+json.dumps(dict(program_realpath=str(program),program_before_sha256=program_before,program_after_sha256=hashlib.sha256(program.read_bytes()).hexdigest(),helper_realpath=str(helper),helper_before_sha256=helper_before,helper_after_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),generated_data_count=len(files),invocation_count=len(evidence),no_generated_file_executed=True),sort_keys=True))
        for row in evidence:print('LIBTREE-COMMAND '+json.dumps(row,sort_keys=True))
        for path in files:
            b=path.read_bytes();print('LIBTREE-INERT-DATA '+json.dumps(dict(path=str(path.relative_to(work)),mode=oct(path.stat().st_mode&0o777),sha256=hashlib.sha256(b).hexdigest(),base64=base64.b64encode(b).decode()),sort_keys=True))
        shutil.rmtree(work)
if __name__=='__main__':main()
LIBTREE_QA
cat > expected-groups.txt <<'LIBTREE_EXPECTED'
ok 1 - version
ok 2 - precise malformed input errors
ok 3 - ELF32 and ELF64 data
ok 4 - dependency class and machine compatibility
ok 5 - original RPATH environment RUNPATH order
ok 6 - bounded long-needed and search-component regressions
libtree-cli: 6 groups passed
LIBTREE_EXPECTED

%build
%set_build_flags
# Upstream adds its c99/Wall/Wextra/Wshadow/pedantic and FILE_OFFSET_BITS flags.
%make_build CC=gcc CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
%make_install PREFIX=%{_prefix}
install -Dpm 0644 regressions.py %{buildroot}%{_libexecdir}/libtree/regressions.py
install -Dpm 0644 expected-groups.txt %{buildroot}%{_datadir}/libtree-tests/expected-groups.txt
install -d %{buildroot}%{_licensedir}/%{name}
cp -a source-notices %{buildroot}%{_licensedir}/%{name}/source-notices
install -pm 0644 LICENSE Apache-2.0.txt %{buildroot}%{_licensedir}/%{name}/

%check
set -eu
export LC_ALL=C LANG=C
# Four original -nostdlib files are inert parser inputs: never execute/install
# them or link them with a 32-bit libc. Only this test's flags use these ISAs.
# Target CI must prove native GCC+ld can generate both ELF classes.
make check CC=gcc ELF32_FLAGS='-march=rv32imac -mabi=ilp32' ELF64_FLAGS='-march=rv64imac -mabi=lp64' > original-check.stdout 2> original-check.stderr || { status=$?; cat original-check.stdout original-check.stderr; exit "$status"; }
cat original-check.stdout original-check.stderr
for dir in tests/01_origin tests/02_rpath_of_parents_parent tests/03_direct_and_absolute_rpath tests/04_rpath_over_env_over_runpath tests/05_32_bits tests/06_symbol_versions tests/07_origin_is_relative_to_symlink_location_not_realpath tests/08_nodeflib tests/10_rpath_order; do
    test -f "$dir/Makefile"
done
for item in exe32 lib32/libx.so exe64 lib64/libx.so; do
    readelf -h "tests/05_32_bits/$item" > "fixture-$(basename "$item")-$(dirname "$item" | tr / _).header"
    grep -Eq 'Machine:[[:space:]]+RISC-V' "fixture-$(basename "$item")-$(dirname "$item" | tr / _).header"
    case "$item" in exe32|lib32/*) class=ELF32 ;; *) class=ELF64 ;; esac
    grep -Eq "Class:[[:space:]]+$class" "fixture-$(basename "$item")-$(dirname "$item" | tr / _).header"
    cat "fixture-$(basename "$item")-$(dirname "$item" | tr / _).header"
done
readelf -d tests/05_32_bits/exe32 > fixture-exe32.dynamic
readelf -d tests/05_32_bits/exe64 > fixture-exe64.dynamic
grep -Fq 'Shared library: [libx.so]' fixture-exe32.dynamic
grep -Fq 'Shared library: [libx.so]' fixture-exe64.dynamic
fixture_root="$PWD/tests/05_32_bits"
grep -E '\((RPATH|RUNPATH)\)' fixture-exe32.dynamic > fixture-exe32.search-path
grep -E '\((RPATH|RUNPATH)\)' fixture-exe64.dynamic > fixture-exe64.search-path
test "$(wc -l < fixture-exe32.search-path)" -eq 1
test "$(wc -l < fixture-exe64.search-path)" -eq 1
grep -Fq "[$fixture_root/lib64:$fixture_root/lib32]" fixture-exe32.search-path
grep -Fq "[$fixture_root/lib32:$fixture_root/lib64]" fixture-exe64.search-path
cat fixture-exe32.dynamic fixture-exe64.dynamic fixture-exe32.search-path fixture-exe64.search-path
python3 ./regressions.py "$PWD/libtree" > strict-cli.stdout 2> strict-cli.stderr || { status=$?; cat strict-cli.stdout strict-cli.stderr; exit "$status"; }
cat strict-cli.stdout strict-cli.stderr
test ! -s strict-cli.stderr
grep -E '^ok [1-6] - |^libtree-cli: 6 groups passed$' strict-cli.stdout > strict-groups.txt
cmp expected-groups.txt strict-groups.txt
# Generated after install-post stripping: bind final installed binary/helper.
(cd %{buildroot}; sha256sum ./usr/bin/libtree ./usr/libexec/libtree/regressions.py ./usr/share/libtree-tests/expected-groups.txt) > %{buildroot}%{_datadir}/libtree-tests/SHA256SUMS

%files
%license %{_licensedir}/%{name}
%doc README.md CHANGELOG.md
%{_bindir}/libtree
%{_mandir}/man1/libtree.1*
%{_libexecdir}/libtree
%{_datadir}/libtree-tests

%changelog
* Tue Oct 27 2026 openEuler RISC-V package contributors - 3.1.1-1
- Preserve original all/install and nine test suites with inert ELF class flags.
- Fix narrow long-path progress/bounds and add six deterministic CLI groups.
