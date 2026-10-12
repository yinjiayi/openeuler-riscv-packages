# SPDX-License-Identifier: Apache-2.0
Name:           python-pydispatcher
Version:        2.0.7
Release:        1%{?dist}
Summary:        Multi-producer multi-consumer in-memory signal dispatch system
License:        BSD-3-Clause AND Python-2.0
URL:            https://github.com/mcfletch/pydispatcher
Source0:        python-pydispatcher-2.0.7.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-coverage
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
Requires:       python3
Requires:       python3-coverage
Requires:       python3-pytest
Requires:       python3-pytest-cov

%description
Multi-producer multi-consumer signal dispatch with weak references and robust calls.

%prep
%setup -q -n pydispatcher-ec403b24e163b926150f2cadaf8e7a8c057f0749
mkdir -p ../pydispatcher-pristine
cp -a . ../pydispatcher-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
cat > Python-LICENSE <<'PSF_LICENSE'
A. HISTORY OF THE SOFTWARE
==========================

Python was created in the early 1990s by Guido van Rossum at Stichting
Mathematisch Centrum (CWI, see http://www.cwi.nl) in the Netherlands
as a successor of a language called ABC.  Guido remains Python's
principal author, although it includes many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for
National Research Initiatives (CNRI, see http://www.cnri.reston.va.us)
in Reston, Virginia where he released several versions of the
software.

In May 2000, Guido and the Python core development team moved to
BeOpen.com to form the BeOpen PythonLabs team.  In October of the same
year, the PythonLabs team moved to Digital Creations (now Zope
Corporation, see http://www.zope.com).  In 2001, the Python Software
Foundation (PSF, see http://www.python.org/psf/) was formed, a
non-profit organization created specifically to own Python-related
Intellectual Property.  Zope Corporation is a sponsoring member of
the PSF.

All Python releases are Open Source (see http://www.opensource.org for
the Open Source Definition).  Historically, most, but not all, Python
releases have also been GPL-compatible; the table below summarizes
the various releases.

    Release         Derived     Year        Owner       GPL-
                    from                                compatible? (1)

    0.9.0 thru 1.2              1991-1995   CWI         yes
    1.3 thru 1.5.2  1.2         1995-1999   CNRI        yes
    1.6             1.5.2       2000        CNRI        no
    2.0             1.6         2000        BeOpen.com  no
    1.6.1           1.6         2001        CNRI        yes (2)
    2.1             2.0+1.6.1   2001        PSF         no
    2.0.1           2.0+1.6.1   2001        PSF         yes
    2.1.1           2.1+2.0.1   2001        PSF         yes
    2.1.2           2.1.1       2002        PSF         yes
    2.1.3           2.1.2       2002        PSF         yes
    2.2 and above   2.1.1       2001-now    PSF         yes

Footnotes:

(1) GPL-compatible doesn't mean that we're distributing Python under
    the GPL.  All Python licenses, unlike the GPL, let you distribute
    a modified version without making your changes open source.  The
    GPL-compatible licenses make it possible to combine Python with
    other software that is released under the GPL; the others don't.

(2) According to Richard Stallman, 1.6.1 is not GPL-compatible,
    because its license has a choice of law clause.  According to
    CNRI, however, Stallman's lawyer has told CNRI's lawyer that 1.6.1
    is "not incompatible" with the GPL.

Thanks to the many outside volunteers who have worked under Guido's
direction to make these releases possible.


B. TERMS AND CONDITIONS FOR ACCESSING OR OTHERWISE USING PYTHON
===============================================================

PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013, 2014, 2015, 2016 Python Software Foundation; All Rights
Reserved" are retained in Python alone or in any derivative version prepared by
Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
-------------------------------------------

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
Individual or Organization ("Licensee") accessing and otherwise using
this software in source or binary form and its associated
documentation ("the Software").

2. Subject to the terms and conditions of this BeOpen Python License
Agreement, BeOpen hereby grants Licensee a non-exclusive,
royalty-free, world-wide license to reproduce, analyze, test, perform
and/or display publicly, prepare derivative works, distribute, and
otherwise use the Software alone or in any derivative version,
provided, however, that the BeOpen Python License is retained in the
Software, alone or in any derivative version prepared by Licensee.

3. BeOpen is making the Software available to Licensee on an "AS IS"
basis.  BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY
DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

5. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

6. This License Agreement shall be governed by and interpreted in all
respects by the law of the State of California, excluding conflict of
law provisions.  Nothing in this License Agreement shall be deemed to
create any relationship of agency, partnership, or joint venture
between BeOpen and Licensee.  This License Agreement does not grant
permission to use BeOpen trademarks or trade names in a trademark
sense to endorse or promote products or services of Licensee, or any
third party.  As an exception, the "BeOpen Python" logos available at
http://www.pythonlabs.com/logos.html may be used according to the
permissions granted on that web page.

7. By copying, installing or otherwise using the software, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1
---------------------------------------

1. This LICENSE AGREEMENT is between the Corporation for National
Research Initiatives, having an office at 1895 Preston White Drive,
Reston, VA 20191 ("CNRI"), and the Individual or Organization
("Licensee") accessing and otherwise using Python 1.6.1 software in
source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, CNRI
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use Python 1.6.1
alone or in any derivative version, provided, however, that CNRI's
License Agreement and CNRI's notice of copyright, i.e., "Copyright (c)
1995-2001 Corporation for National Research Initiatives; All Rights
Reserved" are retained in Python 1.6.1 alone or in any derivative
version prepared by Licensee.  Alternately, in lieu of CNRI's License
Agreement, Licensee may substitute the following text (omitting the
quotes): "Python 1.6.1 is made available subject to the terms and
conditions in CNRI's License Agreement.  This Agreement together with
Python 1.6.1 may be located on the Internet using the following
unique, persistent identifier (known as a handle): 1895.22/1013.  This
Agreement may also be obtained from a proxy server on the Internet
using the following URL: http://hdl.handle.net/1895.22/1013".

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python 1.6.1 or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python 1.6.1.

4. CNRI is making Python 1.6.1 available to Licensee on an "AS IS"
basis.  CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6.1 WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
1.6.1 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 1.6.1,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. This License Agreement shall be governed by the federal
intellectual property law of the United States, including without
limitation the federal copyright law, and, to the extent such
U.S. federal law does not apply, by the law of the Commonwealth of
Virginia, excluding Virginia's conflict of law provisions.
Notwithstanding the foregoing, with regard to derivative works based
on Python 1.6.1 that incorporate non-separable material that was
previously distributed under the GNU General Public License (GPL), the
law of the Commonwealth of Virginia shall govern this License
Agreement only as to issues arising under or with respect to
Paragraphs 4, 5, and 7 of this License Agreement.  Nothing in this
License Agreement shall be deemed to create any relationship of
agency, partnership, or joint venture between CNRI and Licensee.  This
License Agreement does not grant permission to use CNRI trademarks or
trade name in a trademark sense to endorse or promote products or
services of Licensee, or any third party.

8. By clicking on the "ACCEPT" button where indicated, or by copying,
installing or otherwise using Python 1.6.1, Licensee agrees to be
bound by the terms and conditions of this License Agreement.

        ACCEPT


CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
--------------------------------------------------

Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
The Netherlands.  All rights reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
PSF_LICENSE
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*.whl
install -d %{buildroot}%{_datadir}/python-pydispatcher/original
cp -a ../pydispatcher-pristine/. %{buildroot}%{_datadir}/python-pydispatcher/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-pydispatcher/python-pydispatcher-2.0.7.tar.gz
cat > %{buildroot}%{_datadir}/python-pydispatcher/original-files.json <<'JSON'
{".bzrignore": "315723c53ecb43c5d98252b97d597b0e1f5ff6c696bb3dfd9281d18a300d4a33", ".gitignore": "c672d9688a42078e45e549ba237e1043ecdbdbc27f6e40538aa62fd156fbecc0", "MANIFEST.in": "5a076d7204d6f43a82939838e205bd5decce7be9dfde7b9e1c76a1af31270ffa", "README.md": "6f0e44c195fff94f561ca54e41386322683871a14d42c4805138a7f5faa76dda", "covertest.sh": "dc1257ab885ca9af545b685bd7f9b5ddea113747adf09f7cb89cad889ee3eb81", "docs/images/greypinstripe.png": "cf079a0751be9a6882685b5a992930ee7aa6299deba13c984522fdfe34f8e578", "docs/index.html": "5783acff4055ef51e6d506e2315064b6689cd0005be4f4e7741bce0938c40f96", "docs/pydoc/__init__.py": "80d00a2557b62daf610e4b25f6e83d3ee5d420fd40b8a89496a5d609822d14aa", "docs/pydoc/builddocs.py": "af5c03094f7e88b52a2ec57a03e496b0ba7723ef669463c1d020eca150373877", "docs/pydoc/pydispatch.__init__.html": "1545c5fe35443e7849cdb564a89b369eaa4c52114b318274faae37efc2e11f77", "docs/pydoc/pydispatch.dispatcher.html": "84ffed9a6a54c7ebafeecb5b08e1ccb0736139cd23eebbbf9b68d376cf1ca1e2", "docs/pydoc/pydispatch.errors.html": "8cf590f49d1a53e7486f17248ed4d275a5786eec499e6bc17d765cbee54719ab", "docs/pydoc/pydispatch.html": "553a547cba41bf9f7f5f693a00a9f8ca2a4c614da99421df197073f8e4449aea", "docs/pydoc/pydispatch.robust.html": "9cbf7ed2ec87528d353225d5c6a35fe82083fe8970b71ae1464e15fff6f99a8d", "docs/pydoc/pydispatch.robustapply.html": "ab9e75ec13143e7da8c01b400ec6ae37d767ef11e7019a04eb697904d24c7590", "docs/pydoc/pydispatch.saferef.html": "f57e5e5ba1e0077484f90594841a565c4f8e36461ed35926d8e20e1e59f23f3a", "docs/pydoc/pydoc2.py": "177f8adc47d40d83b84d9b519cc0e02056741743b91f8fce59a5b11c4b1d0443", "docs/pydoc/weakref.html": "054a61eebf79d662eb8366db3e294e79d432727cabaa0a6171b3b503fd7905aa", "docs/style/sitestyle.css": "1d196dc1a83a5d9a8ba29ccfc5db94905ab1610c68ad5eee7b90dd7e247a969d", "examples/__init__.py": "9c2dd6c074a010d2d6084def05c8ec3f777699ace3fcfce3f9cd658bb2cbf1a6", "examples/extra_args.py": "b307d970a928f7bd465b6f8ff50e27832dec4b603e0c7b7e38c587bd6fa0d6ea", "examples/hello_messages.py": "6e537986529d445cdfe3c8def3b1faa75e27cddd14f6f01a7242e3f4dbacd02c", "examples/minimal.py": "218a2d4de0222b98d6d08a5496aa9d7f57a4f880df457e9922cf782e7bf01247", "examples/simple_sample.py": "a5290ee857b3eeb0e1a57d6511d709dccffeb2aad40548deed38ecef48465dc5", "license.txt": "aeec9c40c508ce52e66e3eb087c062d8ecf49622a4abd3af79410506b43b698b", "pydispatch/__init__.py": "e9af29ce291575ffd9c603a89b0f2f3dfc1428059dd336bd3887fdaf1c0e35b2", "pydispatch/dispatcher.py": "bc8e84b239fa9aa7f704b22d946db676d5458462e7cd6ed5b93254dff039f584", "pydispatch/errors.py": "98369fb16102b42d0e14ba6024fe4237672ce3ef72f11b64e313b8e115421b3f", "pydispatch/robust.py": "f3fb07f3bdc00e6632a7a5074cbff81209c674c9096f7a6e1e957c36f7e18e3e", "pydispatch/robustapply.py": "813b7811c89c21fd275df396cb2092484dc02afaea82cdca70c29e1c986ea170", "pydispatch/saferef.py": "b673008adc866c07c1f73ed5bc2e136ca41650a2c0db38d79e613300645902bf", "pydispatcher-1.0.0.ebuild": "e4d3056eb4fe54a0eaad26ac9b86bdfb37ab0c674afdb940e2246073ed46ebca", "pydispatcher-2.0.0.ebuild": "d374c99917f65f148a8e4cde5b27a674457086285c9352f6fdab607d442f4e55", "pyproject.toml": "241059177883ecd7c208bf670cce8cc5f7cc44a413dcbbbd6a79c11c49a0dad3", "requirements.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "setup.cfg": "4803547a6818957e2375fa22bc50e9598bac91f09d51c7898c385cbab0cc4a76", "setup.py": "b4ef83c257641406352211a522d33762ebc8c5d1e73cb9a33a9dea02ce5ca558", "test-requirements.txt": "f146a641df65f06654fd79e8939ddc359c939a77f1d2253c10f8f01e76f6ace0", "tests/__init__.py": "81bbee35c8503b64b70f53bbe74cf54a7c075f37d2abea7096ead47d9276f248", "tests/test_dispatcher.py": "53dbe484e3c82e46335af47d9b4e846e6774023aefbbebf70a6acd19258eb2dd", "tests/test_packaging.py": "8887db3fadfc02257b4b86d9e0ad870f5eb6a222f7fbee240fc9f6f7823388a1", "tests/test_robustapply.py": "3d1c26398e7bd1e79e2d0567690934d0be7db853a6260df10632bb85a64396dc", "tests/test_saferef.py": "2d084aaab36c251f2117f651b862ae8a41701b43aeea5d91e0865cc02334b777", "tox.ini": "32ff98f1c9468512240947ee3940958a0bb37c56f854231a992134e177a08b2a", "upload-docs.sh": "ba69c3b7076cdabe28937f79a384207166ad1a4f341d35ae48a3d93a6c30fe9e"}
JSON


%check
%{__python3} - "%{buildroot}%{_datadir}/python-pydispatcher/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,os,pathlib,shutil,subprocess,sys,tempfile
original=pathlib.Path(sys.argv[1]).resolve();site=pathlib.Path(sys.argv[2]).resolve();installed=sys.argv[3]=='installed'
manifest=json.loads((original.parent/'original-files.json').read_text())
runtime={p.removeprefix('pydispatch/'):h for p,h in manifest.items() if p.startswith('pydispatch/')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned(p):
    if installed:assert subprocess.check_output(['rpm','-qf','--qf','%%{NAME}',str(p)],text=True)=='python-pydispatcher'
assert len(manifest)==45 and len(runtime)==6
for p,h in manifest.items():
    q=original/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
for p,h in runtime.items():
    q=site/'pydispatch'/p;assert q.is_file() and not q.is_symlink() and digest(q)==h;owned(q)
if installed:
    archive=original.parent/'python-pydispatcher-2.0.7.tar.gz';assert digest(archive)=='25b3b2b036fc21246c1bad5ba289b29831ed1f128c8fd036faa9cb3f8e7dd565';owned(archive);owned(original.parent/'original-files.json')
for base,expected in ((original,manifest),(site/'pydispatch',runtime)):
    for p in base.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(base).as_posix()
        if rel in expected:continue
        assert p.parent.name=='__pycache__' and p.suffix=='.pyc' and any(p.name.startswith(pathlib.Path(x).stem+'.') and p.parent.parent==base/pathlib.Path(x).parent for x in expected if x.endswith('.py')),rel
        owned(p)
guard="""import hashlib,importlib.abc,importlib.machinery,importlib.metadata,json,pathlib,sys
site=pathlib.Path(SITE_JSON).resolve();expected=json.loads(RUNTIME_JSON)
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='pydispatch' or fullname.startswith('pydispatch.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path);assert spec and spec.origin
            p=pathlib.Path(spec.origin).resolve();rel=p.relative_to(site/'pydispatch').as_posix()
            assert rel in expected and hashlib.sha256(p.read_bytes()).hexdigest()==expected[rel],(fullname,str(p))
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
# No runtime preloading before original pytest-cov instrumentation.
""".replace('SITE_JSON',repr(str(site))).replace('RUNTIME_JSON',repr(json.dumps(runtime)))
with tempfile.TemporaryDirectory(prefix='python-pydispatcher-defaults-') as scratch:
    work=pathlib.Path(scratch)/'original';work.mkdir()
    for p in manifest:
        if p.startswith('pydispatch/'):continue
        dst=work/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/p,dst)
    assert not (work/'pydispatch').exists()
    env=dict(os.environ,PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1')
    args=['--cov=pydispatch','--no-cov-on-fail','--cov-report=term-missing','tests']
    code=guard+'\nimport runpy\nsys.argv='+repr(['pytest']+args)+'\nrunpy.run_module("pytest",run_name="__main__")\n'
    subprocess.run([sys.executable,'-c',code],cwd=work,env=env,check=True)
    # Original packaging test exercises importlib.metadata; verify ownership too.
    code=guard+'\nd=importlib.metadata.distribution("PyDispatcher");assert d.version=="2.0.7";p=pathlib.Path(d._path).resolve();p.relative_to(site);print(str(p))\n'
    metadata_path=pathlib.Path(subprocess.check_output([sys.executable,'-c',code],cwd=work,env=env,text=True).strip())
    for p in metadata_path.rglob('*'):
        if p.is_file():owned(p)
    print(json.dumps({'route':'Original shared tox pytest coverage default on target Python3.11','original_files':len(manifest),'runtime_files':len(runtime),'commands':[['pytest']+args],'runtime_origin':str(site/'pydispatch'),'engine':'installed-RPM' if installed else 'buildroot-wheel','boundary':'Whole tests/defaults retained; no claim about original legacy interpreter matrix, standalone nose coverage utility or native hardware.'}))
PY

%files
%license license.txt Python-LICENSE
%doc README.md
%{python3_sitelib}/pydispatch/
%{python3_sitelib}/[Pp]y[Dd]ispatcher-*.dist-info/
%{_datadir}/python-pydispatcher/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.7-1
- Initial package preserving complete original defaults and BSD notices.
