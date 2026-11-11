#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- sshexec sshexec-tests
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/sshexec/qa/sshexec-1.2.2.tar.gz"
    echo '7f42b9cd096f6bac9c7700f18b1fbe3b6f04091f17b005322158948e771f0d4e  '"$archive" | sha256sum -c -
    python3 -I -B - "$root" <<'PY'
import json, os, pathlib, subprocess, sys, tempfile
root=sys.argv[1]
tool=pathlib.Path(root+'/usr/bin/sshexec').resolve()
sshcd=pathlib.Path(root+'/usr/bin/sshcd')
assert sshcd.is_symlink() and sshcd.resolve()==tool
assert not sys.flags.optimize
with tempfile.TemporaryDirectory(prefix='sshexec-qa-') as tmp:
    work=pathlib.Path(tmp)
    capture=work/'argv.json'
    stub=work/'ssh-stub'
    stub.write_text('#!/usr/bin/python3\nimport json,os,sys\nwith open(os.environ["CAPTURE"],"w") as f: json.dump(sys.argv[1:],f)\nsys.exit(int(os.environ.get("STUB_STATUS","0")))\n')
    stub.chmod(0o755)
    env={'PATH':'/usr/bin:/bin','LC_ALL':'C','SSHEXEC_SSH':str(stub),'CAPTURE':str(capture),'SHELL':'/bin/sh'}
    def run(args, exe=tool, status=0, extra=None):
        if capture.exists(): capture.unlink()
        p=subprocess.run([str(exe),*args],cwd=work,env=dict(env,**(extra or {})),capture_output=True,timeout=15)
        assert p.returncode==status,(args,p.returncode,p.stderr)
        return p,json.loads(capture.read_text()) if capture.exists() else None
    values=['','space x',"a'b",'$HOME;touch should-not-exist','@09','line\n\n','back\\slash']
    values += [chr(i) for i in range(1,128)]
    p,argv=run(['-p','2222','user@host','/usr/bin/printf','%s\\0',*values])
    assert not p.stdout and not p.stderr and argv[:4]==['-p','2222','--','user@host'] and len(argv)==5
    replay=subprocess.run(['/bin/sh','-c',argv[-1]],cwd=work,env=env,capture_output=True,timeout=15)
    assert replay.returncode==0 and not replay.stderr and replay.stdout==b''.join(v.encode()+b'\0' for v in values)
    assert not (work/'should-not-exist').exists()
    p,argv=run(['{','dir=/missing-sshexec-qa','cd=strict','}','host','/usr/bin/printf','ok'])
    assert argv[:2]==['--','host'] and ' && ' in argv[-1]
    strict=subprocess.run(['/bin/sh','-c',argv[-1]],cwd=work,env=env,capture_output=True,timeout=15)
    assert strict.returncode!=0 and not strict.stdout and strict.stderr
    p,argv=run(['{','dir=/missing-sshexec-qa','cd=lax','}','host','/usr/bin/printf','ok'])
    lax=subprocess.run(['/bin/sh','-c',argv[-1]],cwd=work,env=env,capture_output=True,timeout=15)
    assert lax.returncode==0 and lax.stdout==b'ok' and lax.stderr
    p,argv=run(['host'],exe=sshcd)
    assert argv==['-t','--','host','exec "$SHELL" -l']
    p,argv=run(['host'],exe=sshcd,extra={'SSHCD_PTY_ALLOC_FLAG':''})
    assert argv==['--','host','exec "$SHELL" -l']
    for args in ([],['host'],['-p'],['{','cd=invalid','}','host','true'],['{','dir=a','}','host:b','true']):
        p,argv=run(args,status=255)
        assert not p.stdout and p.stderr and argv is None
    p,argv=run(['host','true'],status=23,extra={'STUB_STATUS':'23'})
    assert argv==['--','host','exec env -- true']
print('PASS sshexec downstream ASCII byte roundtrip, options, strict/lax, sshcd and error statuses; SSH stub only')
PY
)
run_installed_tests ''
