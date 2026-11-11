# SPDX-License-Identifier: Apache-2.0
Name:           python-markuppy
Version:        1.18
Release:        1%{?dist}
Summary:        Lightweight HTML and XML generation for Python
License:        MIT AND LicenseRef-Public-Domain AND Apache-2.0
URL:            https://github.com/tylerbakke/MarkupPy
Source0:        markuppy-1.18.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools >= 61.0
BuildRequires:  python3 >= 3.11
BuildRequires:  python3 < 3.12
Requires:       python3 >= 3.11
Requires:       python3 < 3.12

%description
MarkupPy generates HTML and XML from Python programs. The original default
unittest suite and source notices are retained for installed-RPM verification.

%prep
%setup -q -n MarkupPy-abeb20b9a6d0157ea561ab00b21b8e42dc62b086
# GitHub archive group-writability is transport metadata, not a Git mode.
# Preserve source bytes and executable bits while normalizing RPM permissions.
chmod -R go-w .
mkdir -p ../markuppy-pristine
cp -a . ../markuppy-pristine/

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-deps --no-index --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/*arkup*y-1.18-*.whl
install -d %{buildroot}%{_datadir}/python-markuppy/original
cp -a ../markuppy-pristine/. %{buildroot}%{_datadir}/python-markuppy/original/
# Retained sources are data; invoke the original runner with Python, as documented.
# Keeping fixtures non-executable also prevents BRP shebang rewriting their bytes.
find %{buildroot}%{_datadir}/python-markuppy/original -type f -exec chmod 0644 {} +
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-markuppy/markuppy-1.18.tar.gz
cat > %{buildroot}%{_datadir}/python-markuppy/original-files.json <<'JSON'
{".github/workflows/publish.yml": {"mode": 420, "sha256": "1b54f6eb1474047f14d1f0a599dbadbb5162451786e071f7428df4b10472ebcd"}, ".gitignore": {"mode": 420, "sha256": "e4b3654b0ee451c0c00f639b4b1a2ddfed2feab074c3dfd55c14785f77cadf9c"}, "LICENSE": {"mode": 420, "sha256": "947007a0d8b37f4192622a7ddbb2765a65eb73133f77bc423b369075ecf1fb67"}, "MarkupPy/__init__.py": {"mode": 420, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}, "MarkupPy/markup.py": {"mode": 420, "sha256": "03a51440c6bf39f4bb8b27acea43a73acc2e2e44bd8e3d66c0ebcd44fdb23e48"}, "README.md": {"mode": 420, "sha256": "8b6673d5bb0481ded981e820354e985c00a5a35782938aa11b630d98986f6155"}, "_config.yml": {"mode": 420, "sha256": "91330137f6537697be5cf6f4f05651b945d920325cbea69601d95e3d06a68019"}, "pyproject.toml": {"mode": 420, "sha256": "abf339c459bb715e9ef34925590fa2204cb1d7f507ea8fe2ef6842d568494b8e"}, "setup.cfg": {"mode": 420, "sha256": "1cb0362b129e6a8a2ebf05373e78e38716ba1f844e1cd57f4c3fdfd0781a493a"}, "setup.py": {"mode": 420, "sha256": "bc7d808b49bfe9202629bbacd80ac4c2e38aa27f8f2c8dc1c29172ad0b75e53c"}, "tests/run_tests.py": {"mode": 493, "sha256": "87d2d8614476be3b67d1d7e6454ad85a200c8e77291e367de81f0f3961297120"}, "tests/test_add_raw.py": {"mode": 420, "sha256": "892ec4a6f821ae2ef15804de02b1034f9324a5b761915216ea6ca0d41233a860"}, "tests/test_inline_features.py": {"mode": 420, "sha256": "bdefd4600eaa4f49d9b9b0cf8b755e27996327059b8bbb4a457aeadf36a801c0"}}
JSON
cat > %{buildroot}%{_datadir}/python-markuppy/verify.py <<'PY'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
"""Run the unchanged original default suite against staged or RPM-owned code."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def digest(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_results(output):
    """Accept unittest's one- or two-line verbosity while requiring exact IDs."""
    expected = {
        'test_inline_features.TestInlineFeatures.test_combined_features',
        'test_inline_features.TestInlineFeatures.test_script_content_list',
        'test_inline_features.TestInlineFeatures.test_script_content_string',
        'test_inline_features.TestInlineFeatures.test_style_content_list',
        'test_inline_features.TestInlineFeatures.test_style_content_string',
        'test_add_raw.TestAddRaw.test_add_raw_appending',
        'test_add_raw.TestAddRaw.test_add_raw_content_control',
        'test_add_raw.TestAddRaw.test_add_vs_add_raw',
        'test_add_raw.TestAddRaw.test_table_example',
    }
    lines = output.splitlines()
    completed = []
    for i, line in enumerate(lines):
        if not line.startswith('test_'):
            continue
        match = re.fullmatch(r'(test_\w+) \(([^)\n]+)\)(?: \.\.\. (.+))?', line)
        assert match, line
        name, identity, status = match.groups()
        assert identity in expected and identity.rsplit('.', 1)[1] == name, identity
        if status is None:
            assert i + 1 < len(lines), line
            description, separator, status = lines[i + 1].rpartition(' ... ')
            assert separator and description and not description.startswith('test_'), line
        assert status == 'ok', (identity, status)
        completed.append((name, identity))
    assert len(completed) == len(set(completed)) == 9, completed
    assert {identity for _, identity in completed} == expected
    assert len(re.findall(r'^Ran 9 tests in [0-9.]+s$', output, re.M)) == 1
    assert len(re.findall(r'^OK$', output, re.M)) == 1
    assert not re.search(r'\b(?:skipped|FAILED|ERROR|FAIL)\b', output)
    return completed


def main():
    assert len(sys.argv) == 4 and sys.argv[3] in ('buildroot', 'installed')
    assert (3, 11) <= sys.version_info[:2] < (3, 12), sys.version
    root, site = (Path(p).resolve() for p in sys.argv[1:3])
    installed = sys.argv[3] == 'installed'
    manifest = json.loads((root / 'original-files.json').read_text())
    assert len(manifest) == 13
    original = root / 'original'

    def owned(path):
        if installed:
            assert subprocess.check_output(
                ['rpm', '-qf', '--qf', '%%{NAME}', str(path)], text=True
            ) == 'python-markuppy'

    for rel, row in manifest.items():
        p = original / rel
        assert digest(p) == row['sha256'], rel
        # RPM's brp scripts may add bytecode, not change retained source bytes.
        assert row['mode'] in (0o644, 0o755) and p.stat().st_mode & 0o777 == 0o644, rel
        owned(p)
    archive = root / 'markuppy-1.18.tar.gz'
    assert digest(archive) == '9c7ba86d5d9fb7b2b4be71c55496a18742c300eeff08e3e07895e92db07fc98d'
    owned(archive)
    owned(root / 'original-files.json')
    owned(root / 'verify.py')
    runtime = {p.removeprefix('MarkupPy/'): r['sha256']
               for p, r in manifest.items() if p.startswith('MarkupPy/')}
    assert set(runtime) == {'__init__.py', 'markup.py'}
    for rel, expected in runtime.items():
        p = site / 'MarkupPy' / rel
        assert digest(p) == expected, str(p)
        owned(p)
    distributions = [d for d in importlib.metadata.distributions(path=[str(site)])
                     if re.sub(r'[-_.]+', '-', d.metadata['Name']).lower() == 'markuppy']
    assert len(distributions) == 1 and distributions[0].version == '1.18'
    for name in ('METADATA', 'WHEEL', 'RECORD'):
        owned(distributions[0]._path / name)
    # Fail closed for a new unexpected runtime source; normal RPM bytecode is allowed.
    for p in (site / 'MarkupPy').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(site / 'MarkupPy').as_posix()
        assert rel in runtime or (p.parent.name == '__pycache__' and
               p.suffix == '.pyc' and any(p.name.startswith(Path(x).stem + '.')
                                         for x in runtime)), rel
        owned(p)

    guard = '''import hashlib,importlib.abc,importlib.machinery,pathlib,sys,runpy
site=pathlib.Path(SITE);runtime=RUNTIME
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='MarkupPy' or fullname.startswith('MarkupPy.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path)
            assert spec and spec.origin,(fullname,spec)
            p=pathlib.Path(spec.origin).resolve()
            rel=p.relative_to(site/'MarkupPy').as_posix()
            assert rel in runtime and hashlib.sha256(p.read_bytes()).hexdigest()==runtime[rel]
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
sys.path.insert(0,str(site))
sys.path.insert(0,TESTS)
sys.argv=[RUNNER]
runpy.run_path(RUNNER,run_name='__main__')
'''.replace('SITE', repr(str(site))).replace('RUNTIME', repr(runtime))
    with tempfile.TemporaryDirectory(prefix='markuppy-original-defaults-') as scratch:
        work = Path(scratch)
        tests = work / 'tests'
        tests.mkdir()
        for rel, row in manifest.items():
            if rel.startswith('tests/'):
                shutil.copyfile(original / rel, work / rel)
                assert digest(work / rel) == row['sha256']
        assert len(list(tests.iterdir())) == 3 and not (work / 'MarkupPy').exists()
        runner = tests / 'run_tests.py'
        code = guard.replace('TESTS', repr(str(tests))).replace('RUNNER', repr(str(runner)))
        env = {k: v for k, v in os.environ.items()
               if not k.startswith('PYTHON') and k not in ('HOME',)}
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run([sys.executable, '-I', '-B', '-c', code], cwd=work,
                                env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False)
        print(result.stdout, end='')
        assert result.returncode == 0, result.returncode
        completed = original_results(result.stdout)
        assert len(completed) == len(set(completed)) == 9, completed
        assert re.search(r'^Ran 9 tests in ', result.stdout, re.M)
        assert re.search(r'^OK\s*$', result.stdout, re.M)
        assert not re.search(r'\b(?:skipped|FAILED|ERROR|FAIL)\b', result.stdout)
    for rel, expected in runtime.items():
        assert digest(site / 'MarkupPy' / rel) == expected
    print(json.dumps(dict(original_default_runner='tests/run_tests.py', tests=9,
                          skips=0, runtime_origin=str(site / 'MarkupPy'),
                          engine='installed-RPM' if installed else 'buildroot-wheel',
                          python=sys.version.split()[0])))


if __name__ == '__main__':
    main()
PY
cat > QA-LICENSE <<'LICENSE'
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
LICENSE
cat > UPSTREAM-NOTICES <<'NOTICE'
MarkupPy 1.18, fixed upstream abeb20b9a6d0157ea561ab00b21b8e42dc62b086.
The complete upstream MIT text is installed as LICENSE. The original runtime
MarkupPy/markup.py additionally contains Daniel Nogradi's public-domain grant:
# This code is in the public domain, it comes
# with absolutely no warranty and you can do
# absolutely whatever you want with it.
Its complete original header, authors and documentation remain in the runtime
and retained original source; LicenseRef-Public-Domain denotes that explicit
grant, not an assertion that upstream used the Unlicense or CC0 text.
Separately authored installed verification code is Apache-2.0, not upstream
MarkupPy code; its complete license is installed as QA-LICENSE.
NOTICE

%check
%{__python3} -I -B %{buildroot}%{_datadir}/python-markuppy/verify.py %{buildroot}%{_datadir}/python-markuppy %{buildroot}%{python3_sitelib} buildroot

%files
%license LICENSE UPSTREAM-NOTICES QA-LICENSE
%doc README.md
%{python3_sitelib}/MarkupPy/
%{python3_sitelib}/*arkup*y-1.18.dist-info/
%{_datadir}/python-markuppy/

%changelog
* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.18-1
- Preserve all nine original default tests and verify staged and installed origins.
