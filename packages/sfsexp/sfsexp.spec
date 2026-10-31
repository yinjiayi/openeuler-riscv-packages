# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors.
# Full Apache-2.0 text is Source2; compiled library terms are distinct.
Name:           sfsexp
Version:        1.4.1
Release:        1%{?dist}
Summary:        Small and fast S-expression C library
License:        LGPL-2.1-or-later AND LicenseRef-SFSEXP-GNU-Helpers AND X11 AND FSFAP AND Apache-2.0
URL:            https://github.com/mjsottile/sfsexp
Source0:        https://github.com/mjsottile/sfsexp/releases/download/v1.4.1/sfsexp-1.4.1.tar.gz
Source1:        https://www.gnu.org/licenses/gpl-3.0.txt#/GPL-3.0.txt
Source2:        https://www.apache.org/licenses/LICENSE-2.0.txt#/Apache-2.0.txt

BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gcc
Requires:       glibc-devel
Requires:       grep
Requires:       pkgconf-pkg-config
Requires:       python3

%description
S-expression parsing, printing, continuations, binary atoms and tree operations.
One deliberate SDK package retains the original shared/static library, headers
and pkg-config file. Examples and eight upstream test programs remain built
but uninstalled. Original make check has zero registered functional tests.
Six deterministic original binaries and six owned public API groups provide
additional functional checks; timing/watchdog and Valgrind matrices are not
claimed to have run. No native performance or thread-safety claim is made.

%prep
%setup -q -n sfsexp-%{version}
test ! -e packaging-qa
test ! -e packaging-notices
test ! -e packaging-source.sha256
python3 - <<'PY_ORIGINAL'
import hashlib, json, shutil
from pathlib import Path
original = json.loads(r'''{
  "COPYING": "11b3496d16e0b24cce33316132bd52a1bce896b683b2ef1b86adfbfd102dc991",
  "Doxyfile": "1008640d4f8257f43adf200ff0442738b4c3d38441dc9e0f60829265396ad5d0",
  "INSTALL": "c5bcdf3e7704df37f8379847d57d2ccc2092089d71215e5885d78c7477e622ba",
  "LICENSE_LGPL": "f855e98cbf0e1abbd258282c10690b47b23568b60eb62a3e270ad4a780304afa",
  "Makefile.am": "8497342ed357659bd03ff8eac2dd09a59f3a110bdcd0686920afce1718329e8e",
  "Makefile.in": "e254aeb4e6d7d86ae71106eacb417ad97f2b5de87c94cd341977719d4f1c8602",
  "README.md": "691de14131d7e88ee2223de153b908584de93bf408da56ecfe19ad370c6031e8",
  "README_cmake.txt": "41aa0a04b784cb9df08fcf86f25cdd0dc07282cff32f418d02cc2e7ec4c01b88",
  "aclocal.m4": "a036b838ae98a4315742b1840360de7ffacb618535687e87a4d1d7473290a2da",
  "compile": "c207b390aac6323062b982214a6c63448e53e6911107993abe96f35fe7a30a18",
  "config.guess": "af8a1922c9b3c240bf2119d4ec0965a0b5ec36b1016017ba66db44b3b53e9cea",
  "config.h.in": "643ece80cb2d6b2ec16033903d97fc3c78538f00a7208ba545d6050acf1ec00f",
  "config.sub": "d611751fba98e807c9684d253bb02aa73d6825fe0e0b9ae3cbf258a59171c9b0",
  "configure": "060a9901a8cd689b0e578dd21920e97629808c09461076cc6f294ab22553f0a4",
  "configure.ac": "9e73e508581e9e667fdb0ddc6c3a1db91abf909f47e7d980d24d615e3491fd10",
  "depcomp": "e44b49f71b265788187993090027193a6cd2b4718f9aa7be34412f537bce6873",
  "examples/Makefile.am": "c5bca8e9bf20387aa6e50e008547342efacdba7660c446d07d583be113539014",
  "examples/Makefile.in": "e2c1123fde5396a10c904b50d53d7b5e2ab6590cffd84d113064b9be2abafad4",
  "examples/binmode.c": "c8f006f83b6676e300cf1fba1446f84ce0a38127933399a7d7a8dc606784da74",
  "examples/callbacks.c": "80ee5d7735e61f885a4e9f00acf43b6ded89e35b50891084a36b86123004ec4d",
  "examples/continuations.c": "bed77e6b193f4c128729421adb9426f8d354aba236b01dd3fce8c1cfe306074f",
  "examples/conttest": "8eaac3573e363784c28cbb194eccd1cd7d8d268c1b7a31c8168c2b9b9e9381ee",
  "examples/edgelist.dat": "d24496fc85dfc254147522a0e96cfa2ba552d802ccbb2b31bd4d377ea4138f1c",
  "examples/packunpack.c": "92367b413f23267daef1fc0d766fb84dd958e7bb7f0fb71562fad4d9fce30781",
  "examples/paultest.c": "d650711a7c27ef05c8ba98ba632af3a080d92b71ff1b27bee9f6ff55aeed4d2d",
  "examples/rcfile.c": "da27922f4b4ae52bc54f3f42a94040bb062fd22246243e5bfd6cdcef5b411b37",
  "examples/sexps.in": "f0cbd910fdd8c25bccda323e94c61ecafd6d7b35dcd896b49adc153b7cd92e1d",
  "examples/sexpvis.c": "d9110ae8e8c3da36d3ac0de9b66eb9537735843a5004ff19390918c6fed82a18",
  "examples/simple_interp.c": "f2290c9728f007257b761071a0247c064a090131d8b613ad4055f2cd00194dd6",
  "examples/testrc": "1bc32c462b649f922ab0ca0f3daa52b8718ebf316d8ed5edba814da85d65da92",
  "examples/vis.in": "9162ac19f5ab380be91766cb09cfa179655bf3edfe37e24a55e042e9312dbc38",
  "install-sh": "3d7488bebd0cfc9b5c440c55d5b44f1c6e2e3d3e19894821bae4a27f9307f1d2",
  "ltmain.sh": "76d58793835f70be2fe69308f0f62b2ff07edd5c45f5255ed42265e147693761",
  "m4/libtool.m4": "6847305792cd3ff45efda8f8c703c8a29cbe34718ef0ed0c74ef41db871f4c43",
  "m4/ltoptions.m4": "f3d4ed0426501308028dd7690cf343cb280479d637a2ebee6c289ec2e708df3b",
  "m4/ltsugar.m4": "0896f153a5a40546566028a4272642ae291532f3e65c25fcae950c8812b8c265",
  "m4/ltversion.m4": "2a6baf40b64f34234e0b76c7ff62b01a1f6bbf60089f4f74506b49f800ffaf9e",
  "m4/lt~obsolete.m4": "8533006830e1ea9625fc5e4c060e653eedf9d5464a9b2f5f494244ee272e2e2f",
  "missing": "a9865db4f39574ff128c0312c367f070d20f81847817021ecce95fd70a610c9d",
  "sfsexp.pc.in": "a2edabed966c81a970fb1c27caaec9d8589418bb34aa84f6b743ff2b47bf2428",
  "src/Makefile.am": "54c75d3661a15502e5f4b6f4da3ac915b1024e6e9ee09c8f2cab5dfa10f75679",
  "src/Makefile.in": "c606db040dae346b7e6c39ce6b903f9e42095f44e79e31538bd8a456bdb35fb7",
  "src/cstring.c": "1c8a6cec44945c768c7d06e00d668564dc4f2bad4639ea4c496fa679c0d202e9",
  "src/cstring.h": "7156db819311f6d0ec8de940f1fa86e85a683cc94b90394ed662712c6dd72119",
  "src/event_temp.c": "80c2b61544972ca8ade9ef17a25df70bee86f72332fc0d5984bda5f9775b6c74",
  "src/faststack.c": "f8e0b8ec904cde7085900822b0f85f21551085203ce71b12b053d637f30648f9",
  "src/faststack.h": "4a6e8c4a1a5d615be779f7803d34c60a3af1090d0a4ea93a2ee27f20ea1dbebe",
  "src/io.c": "6157bc200212697d79fcaddede6d985e67983c8487175a5ae2de4e9fa1d82852",
  "src/parser.c": "92d2756f9403cce29ae8f7b87a914a352940b7e4cc354f87b1468f6b267093d5",
  "src/sexp.c": "e480c6743ffe43b1c978428a69d07d46ba94efdc59cedaa965a40e7265b0fe16",
  "src/sexp.h": "474ce7359418e8919f04596e16cd5a24fe81f5708b98c294135fadf8eda8d388",
  "src/sexp_errors.h": "ec043c0349104b764bef096dd65bc895615548fa8701ab8a94af6a4511eccad2",
  "src/sexp_memory.c": "1bf621e91314aaef964ab64f2c12cb531981f918927e8fbbe6c57e638191d5c2",
  "src/sexp_memory.h": "113bace4e4ef641f92d3ce05a12693c01dbf144c6e829ea0487f89e2d5a86e92",
  "src/sexp_ops.c": "b4db3e084c348dda8a994ff2aa2f52feb730bb6f75d39f2ef6872fa576c848eb",
  "src/sexp_ops.h": "167fcc623af863eec6ba228523bc0c923190ba34aa431963c8fec545fbf9dbb3",
  "src/sexp_vis.c": "be4148175940502a6400d8aeb79fa75075e92cf9fb96a3b6e601e87cccee1480",
  "src/sexp_vis.h": "c9297d63dad1b3fa655d789929df7d6bde0e4d48cf007559196ea501e3797ebb",
  "tests/Makefile.am": "a057696e8d76a395f1a1718a8bb7a298abda543eb0b89a211afcb7451a4effab",
  "tests/Makefile.in": "2fba6c17157ae509e2bdc6b194bdb1c497d5f9da0eb748c87e44e6b9abec7ccb",
  "tests/README": "0b8eb25ac7af83188acd36b93a85bddcd5292d1a8e5a89661e53c6a9b6f73328",
  "tests/bug.c": "d45eca0c57f82c4b006836b3c3dc277d814e2d5846598f7d570329fe042093f9",
  "tests/ctest.c": "25e35481149ed4d866c62dbfd723b772546b4ad2a7a5c6f93640588834b912bb",
  "tests/ctorture.c": "2d07480e6ccb344e431c12f842a94a2052082c8b754b3698e113b8592a46255e",
  "tests/dotests.sh": "c483a5b6a45538c1d64d4e501fe4f25e3912be7ae6c848b3e2e7336cca1fa06e",
  "tests/error_codes.c": "66b7a9c2dea593004dbc53e9858139f08aeb21cb20a063838619da9c89fdec2c",
  "tests/partial.c": "394a69af7769d43b1deb5d3088e2cfbd85e1c512e7e490593d6f33a120a502b2",
  "tests/randsexp.pl": "4be22e801aeb1d4edd97f463b2f7e7e31b5f36012e41d027b671889c2feda1f8",
  "tests/read_and_dump.c": "4f58ff27b71689790ee4e78931bdf6fad8c339e1822511ece7da9e61f593e817",
  "tests/readtests.c": "200ef63299b59697b8ed365e38e9949b64ef156c65c0f6ee2050bf940584c768",
  "tests/test_expressions": "1509d63772cf0054d3014762a92e80ddc6862589ece215d6c900a656ba22a80d",
  "tests/vis_test.c": "a460fd858ab2e62818065904e8ca4d6e757b9b42c33f1fea136ade09fd2d36ef",
  "win32/README.txt": "95beb62eeb33e81df362cb89ac97bbb9caffb45cabed9c14df2a2b61af3d74d2",
  "win32/libsexpr/README.txt": "a989a0591d97635f1a4c0c302425c044055299a368551eb992136e82ec1884dd",
  "win32/libsexpr/libsexpr.vcproj": "182890a96eeca7cad251f957327b989862ab3143275796bc1a7b65e6caaac54a",
  "win32/sexpr_test.sln": "fc8349c20946615ebc2bcb61e466d776cb5dbc2a0f991dcb01df195641f09e18",
  "win32/sexpr_test.suo": "16cc982cda422cec8b2a198ab5cf72cf783116dce1d2779174eff7cea173ab2c",
  "win32/sexpr_test/sexpr_test.cpp": "695034913b21a756adbaa6ab18af853249303a509a05a795b8d3441734a429b2",
  "win32/sexpr_test/sexpr_test.vcproj": "f3c68fd245c8b70cf7cc01d06e568967b9ab91492912cbe48e9998412242242f",
  "win32/sexpr_test/stdafx.cpp": "368fb0a12b0754cbe8a26ecd1254d59fbb72f2f7c443de60c55fa4d11bae2099",
  "win32/sexpr_test/stdafx.h": "a03b935a958a9cbff11b5ed10058218b4af26818bad0affefc13e187a0aa5d5a"
}''')
assert len(original) == 81
assert set(original) == {str(p) for p in Path('.').rglob('*') if p.is_file()}
for name, digest in original.items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
Path('packaging-notices').mkdir()
for name in original:
    target = Path('packaging-notices') / (name + '.notice')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(name, target)
Path('packaging-source.sha256').write_text(''.join(digest + '  ' + name + '\n' for name, digest in original.items()))
Path('packaging-notices/SHA256SUMS').write_text(''.join(digest + '  ' + name + '.notice\n' for name, digest in original.items()))
PY_ORIGINAL
mkdir packaging-qa
cat > packaging-qa/consumer.c <<'EOF_CONSUMER'
/* SPDX-License-Identifier: Apache-2.0
 * Copyright 2026 openEuler RISC-V package contributors.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy at https://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. The full text accompanies this source.
 */
#include <sexp.h>
#include <sexp_ops.h>
#include <sexp_memory.h>
#include <sexp_errors.h>
#include <sexp_vis.h>
#include <cstring.h>
#include <faststack.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#ifdef NDEBUG
#error "The package QA requires active assertions."
#endif

static void printed(sexp_t *sx, const char *expected) {
    char out[256];
    assert(sx != NULL);
    assert(print_sexp(out, sizeof out, sx) >= 0);
    assert(strcmp(out, expected) == 0);
}

int main(void) {
    char source[] = "(alpha (beta gamma) delta)";
    sexp_t *sx = parse_sexp(source, strlen(source));
    assert(sx && sx->ty == SEXP_LIST && sexp_list_length(sx) == 3);
    assert(find_sexp("gamma", sx) && bfs_find_sexp("delta", sx));
    assert(find_sexp("absent", sx) == NULL);
    printed(sx, source);
    puts("01 parse-list-search OK");

    sexp_t *copy = copy_sexp(sx);
    assert(copy && copy != sx && copy->list != sx->list);
    destroy_sexp(sx);
    printed(copy, source);
    destroy_sexp(copy);
    puts("02 independent-copy OK");

    sexp_t *basic = new_sexp_atom("alpha", 5, SEXP_BASIC);
    sexp_t *quoted = new_sexp_atom("two words", 9, SEXP_DQUOTE);
    assert(basic && quoted && basic->aty == SEXP_BASIC && quoted->aty == SEXP_DQUOTE);
    basic->next = quoted;
    sx = new_sexp_list(basic);
    printed(sx, "(alpha \"two words\")");
    destroy_sexp(sx);
    puts("03 owned-atoms-list OK");

    char *data = malloc(4);
    assert(data);
    memcpy(data, "a\0b\377", 4);
    sx = new_sexp_binary_atom(data, 4); /* constructor takes this heap allocation */
    assert(sx && sx->aty == SEXP_BINARY && sx->binlength == 4);
    copy = copy_sexp(sx);
    assert(copy && copy->bindata != sx->bindata && copy->binlength == 4);
    assert(memcmp(copy->bindata, data, 4) == 0);
    destroy_sexp(sx);
    assert(memcmp(copy->bindata, "a\0b\377", 4) == 0);
    destroy_sexp(copy);
    puts("04 binary-copy-ownership OK");

    char left[] = "(one ", right[] = "(two) three)";
    pcont_t *pc = cparse_sexp(left, strlen(left), NULL);
    assert(pc && pc->last_sexp == NULL && pc->error == SEXP_ERR_INCOMPLETE);
    pc = cparse_sexp(right, strlen(right), pc);
    assert(pc && pc->last_sexp && pc->error == SEXP_ERR_OK);
    printed(pc->last_sexp, "(one (two) three)");
    destroy_sexp(pc->last_sexp);
    destroy_continuation(pc);
    puts("05 continuation OK");

    CSTRING *str = snew(2);
    assert(str);
    str = sadd(str, "ab");
    assert(str);
    str = saddch(str, 'c');
    assert(str && strcmp(toCharPtr(str), "abc") == 0);
    sempty(str);
    assert(str->curlen == 0);
    sdestroy(str);
    faststack_t *stack = make_stack();
    assert(stack && empty_stack(stack));
    int payload = 42;
    stack = push(stack, &payload);
    assert(stack && stack->height == 1 && top_data(stack) == &payload);
    assert(pop(stack)->data == &payload && empty_stack(stack));
    destroy_stack(stack);
    sexp_errno = SEXP_ERR_OK;
    assert(new_sexp_atom("x", 1, SEXP_BINARY) == NULL);
    assert(sexp_errno == SEXP_ERR_BAD_CONSTRUCTOR);
    sexp_cleanup();
    puts("06 cstring-stack-errors OK");
    return 0;
}
EOF_CONSUMER
cat > packaging-qa/run-qa.py <<'EOF_QA'
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy at https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. The full text accompanies this source.
"""Target-only public SDK checks. Inspection must not execute this file."""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

mode, base = sys.argv[1:]
assert mode in ('build', 'installed')
base = Path(base).resolve(strict=True)
qa = base / 'packaging-qa' if mode == 'build' else base
consumer = qa / 'consumer.c'
headers = 'sexp.h sexp_vis.h sexp_ops.h sexp_memory.h sexp_errors.h cstring.h faststack.h'.split()
library = (base / 'src/.libs/libsexp.so.1.0.0' if mode == 'build' else Path('/usr/lib64/libsexp.so.1.0.0')).resolve(strict=True)
private = Path(tempfile.mkdtemp(prefix='sfsexp-qa-'))
env = dict(os.environ, LC_ALL='C', LANG='C')
for name in ('LD_LIBRARY_PATH', 'LD_PRELOAD', 'LD_AUDIT', 'LD_DEBUG', 'LD_BIND_NOW', 'LIBRARY_PATH', 'CPATH', 'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'PKG_CONFIG_PATH', 'PKG_CONFIG_LIBDIR', 'CFLAGS', 'LDFLAGS'):
    env.pop(name, None)
commands = []
tracked = [consumer, Path(__file__).resolve(), qa / 'expected.stdout', library]
tracked += [base / 'src' / h for h in headers] if mode == 'build' else [Path('/usr/include/sfsexp') / h for h in headers]
if mode == 'installed':
    tracked += [Path('/usr/lib64') / p for p in ('libsexp.so', 'libsexp.so.1', 'libsexp.a', 'libsexp.la', 'pkgconfig/sfsexp.pc')]
def hashes():
    return {str(p): {'realpath': str(p.resolve(strict=True)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in tracked}
before = hashes()
def run(label, argv, extra=None, success=True):
    actual_env = dict(env)
    if extra:
        actual_env.update(extra)
    p = subprocess.run(argv, cwd=private, env=actual_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    for stream in ('stdout', 'stderr'):
        (private / (label + '.' + stream)).write_bytes(getattr(p, stream))
    commands.append({'label': label, 'argv': argv, 'cwd': str(private), 'environment_overrides': extra or {}, 'exit': p.returncode,
        'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(p.stderr).hexdigest(),
        'stdout_base64': base64.b64encode(p.stdout).decode(), 'stderr_base64': base64.b64encode(p.stderr).decode()})
    if success:
        assert p.returncode == 0, (label, p.returncode)
    return p
def same(path):
    try:
        return Path(path).is_file() and os.path.samefile(path, library)
    except OSError:
        return False
def prove_link_paths(trace, linkmap):
    assert any(same(line.strip()) for line in trace.decode().splitlines()), 'trace must name the same library file'
    loads = re.findall(r'^LOAD (.+)$', linkmap.decode(), re.M)
    assert any(same(path.strip()) for path in loads), 'map LOAD must name the same library file'
try:
    if mode == 'installed':
        flags = run('pkgconfig-cflags', ['pkg-config', '--cflags', 'sfsexp'])
        libs = run('pkgconfig-libs', ['pkg-config', '--libs', 'sfsexp'])
        assert flags.stderr == libs.stderr == b''
        cflags, ldflags = shlex.split(flags.stdout.decode()), shlex.split(libs.stdout.decode())
        assert '-lsexp' in ldflags
    else:
        cflags, ldflags = ['-I' + str(base / 'src')], ['-L' + str(library.parent), '-lsexp']
    common = ['gcc', '-std=c11', '-Wall', '-Wextra', '-Werror', *cflags, str(consumer)]
    negative = private / 'negative'
    n = run('negative-no-library', [*common, '-o', str(negative)], success=False)
    assert n.returncode != 0 and n.stdout == b'' and not negative.exists()
    assert b'undefined reference' in n.stderr
    for symbol in (b'parse_sexp', b'print_sexp', b'copy_sexp', b'new_sexp_binary_atom', b'cparse_sexp', b'make_stack'):
        assert symbol in n.stderr
    binary = private / 'consumer'
    linkmap = private / 'consumer.map'
    linked = run('positive-link', [*common, '-Wl,-t,-Map,' + str(linkmap), *ldflags, '-o', str(binary)])
    assert linked.stderr == b''
    mapping = linkmap.read_bytes()
    prove_link_paths(linked.stdout, mapping)
    commands.append({'label': 'full-link-map', 'path': str(linkmap), 'sha256': hashlib.sha256(mapping).hexdigest(), 'base64': base64.b64encode(mapping).decode()})
    elf = run('readelf', ['readelf', '-h', '-d', str(binary)])
    assert elf.stderr == b'' and b'RISC-V' in elf.stdout and b'[libsexp.so.1]' in elf.stdout
    assert b'RPATH' not in elf.stdout and b'RUNPATH' not in elf.stdout
    exports = run('exports', ['nm', '-D', '--defined-only', str(library)])
    assert exports.stderr == b''
    anchors = ('parse_sexp', 'print_sexp', 'copy_sexp', 'new_sexp_binary_atom', 'cparse_sexp', 'make_stack')
    for name in anchors:
        assert re.search(rb'\b' + name.encode() + rb'$', exports.stdout, re.M)
    runtime = {'LD_LIBRARY_PATH': str(library.parent)} if mode == 'build' else {}
    result = run('consumer', [str(binary)], runtime)
    assert result.stderr == b'' and result.stdout == (qa / 'expected.stdout').read_bytes()
    loader = run('loader', [str(binary)], dict(runtime, LD_DEBUG='bindings,libs', LD_BIND_NOW='1'))
    assert loader.stdout == result.stdout
    for name in anchors:
        lines = [line for line in loader.stderr.decode().splitlines() if re.search(r"symbol [`']" + name + r"['`]", line)]
        assert any((m := re.search(r' to (.+?) \[\d+\]', line)) and same(m.group(1)) for line in lines), ('loader binding', name)
    assert before == hashes()
finally:
    record = {'mode': mode, 'private_evidence_directory': str(private), 'program': str(private / 'consumer'), 'program_sha256': hashlib.sha256((private / 'consumer').read_bytes()).hexdigest() if (private / 'consumer').exists() else None, 'inputs_before': before, 'inputs_after': hashes(), 'commands': commands}
    (private / 'qa.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, sort_keys=True))
print('SFSEXP SDK: six public API groups; exact shared-file map/trace/loader bindings; negative link control')
EOF_QA
cat > packaging-qa/original-oracles.py <<'EOF_ORIGINAL'
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy at https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. The full text accompanies this source.
"""Target-only additive oracles; never execute this during source inspection.
Original eight built test binaries are unmodified; six deterministic programs
are invoked here. ctorture timing and vis_test's one-second watchdog are
built but not executed by this additive check. No claim that their
unregistered make-check target or developer Valgrind matrix is functional QA.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve(strict=True)
out = Path(sys.argv[2]).resolve()
assert not out.exists()
out.mkdir(mode=0o700)
tests = root / 'tests'
fixture = tests / 'test_expressions'
assert hashlib.sha256(fixture.read_bytes()).hexdigest() == '1509d63772cf0054d3014762a92e80ddc6862589ece215d6c900a656ba22a80d'
env = dict(os.environ, LC_ALL='C', LANG='C')
records = []
def run(name, argv, stdin=None):
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [tests / '.libs' / name, fixture]}
    p = subprocess.run(argv, cwd=tests, env=env, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    (out / (name + '.stdout')).write_bytes(p.stdout)
    (out / (name + '.stderr')).write_bytes(p.stderr)
    after = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in before}
    assert before == after
    records.append({'name': name, 'argv': argv, 'cwd': str(tests), 'LC_ALL': 'C', 'LANG': 'C', 'exit': p.returncode, 'inputs_before_and_after': before,
        'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(p.stderr).hexdigest(),
        'stdout_base64': base64.b64encode(p.stdout).decode(), 'stderr_base64': base64.b64encode(p.stderr).decode()})
    assert p.returncode == 0, (name, p.returncode)
    assert p.stderr == b'', (name, p.stderr)
    return p.stdout

try:
    b = run('readtests', ['./readtests'])
    matches = re.findall(rb'TOTAL TESTS: (\d+)  PASS=(\d+) FAIL=(\d+)', b)
    assert matches == [(b'18', b'18', b'0'), (b'18', b'18', b'0')]
    assert b'FIXED POINT MISSED' not in b and b'ERROR' not in b
    b = run('ctest', ['./ctest'])
    raw = b"(i am the test '(expression) \"with\" 'weird atoms)"
    matches = re.findall(rb'^(\d+) :: (.*)$', b, re.M)
    assert matches == [(str(i).encode(), raw) for i in range(len(raw), 0, -1)]
    assert all(re.fullmatch(rb'\.*|\d+ :: .*', line) for line in b.splitlines())
    expected = (b'cparse reacted properly to null string.\nerr=4\n'
                b'print_sexp reacted correctly to buffer with insufficient space.\nerr=8\n'
                b'print_sexp_cstr reacted correctly to NULL sexp_t.\nerr=0\n'
                b'(I am a (test))\n')
    assert run('error_codes', ['./error_codes']) == expected
    b = run('partial', ['./partial'])
    assert b.startswith(b'Incomplete expression detected.\n') and len(b.splitlines()) == 2
    assert b'Unexpected error' not in b
    assert run('bug', ['./bug']) == b'(i a\nsexp_errno: 8\n'
    b = run('read_and_dump', ['./read_and_dump'])
    assert len(b.splitlines()) == 18 and all(line.startswith(b'READ: ') and len(line) > 6 for line in b.splitlines())
finally:
    (out / 'original-command-records.json').write_text(json.dumps(records, indent=2) + '\n')
    for row in records:
        print(json.dumps(row, sort_keys=True))
assert len(records) == 6
print('SFSEXP additive original-binary checks: 6 invoked; readtests18+18; continuation chunks all; timing/watchdog and Valgrind matrix not executed')
EOF_ORIGINAL
cat > packaging-qa/expected.stdout <<'EOF_EXPECTED'
01 parse-list-search OK
02 independent-copy OK
03 owned-atoms-list OK
04 binary-copy-ownership OK
05 continuation OK
06 cstring-stack-errors OK
EOF_EXPECTED
cat > packaging-qa/HELPER-LICENSE-NOTE.txt <<'EOF_LICENSE'
LicenseRef-SFSEXP-GNU-Helpers is the following bounded source-helper choice,
not a claim that the compiled SFSEXP library is GPL licensed:
For bundled GNU helper scopes licensed GPL2-or-later or GPL3-or-later,
redistribute under their permitted GPL3-or-later branch with every original
Autoconf/Libtool distribution exception retained. Nested Bootstrap ltmain
snippets use their GPL2-or-later branch (elect GPL3), not an inferred MIT grant.
The full GPL3 text accompanies all 81 unmodified raw original notices.
Other source scopes retain full X Consortium, FSF unlimited-permission and
associated project notices. The core library remains LGPL2.1-or-later.
The optional omitted UTF-8 Git fixture is not added or redistributed here.
EOF_LICENSE
sha256sum -c packaging-source.sha256

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
# The original 81-file manifest remains the pre-configure source boundary.
sha256sum -c packaging-source.sha256
%configure
# Only the three helpers changed by the trusted openEuler macro become typed
# build inputs. Their raw original notices and original hashes remain intact.
python3 - <<'PY_BUILD_INPUTS'
import hashlib, json, os
from pathlib import Path
digest = lambda data: hashlib.sha256(data).hexdigest()
original = dict(line.split('  ', 1)[::-1] for line in Path('packaging-source.sha256').read_text().splitlines())
helpers = {'config.guess', 'config.sub', 'ltmain.sh'}
assert len(original) == 81 and helpers <= set(original)
for name, expected in original.items():
    assert digest(Path('packaging-notices', name + '.notice').read_bytes()) == expected, name
    if name not in helpers:
        assert digest(Path(name).read_bytes()) == expected, name
provenance = {}
for name in ['config.guess', 'config.sub']:
    system = Path('/usr/lib/rpm/openEuler') / name
    assert Path(name).read_bytes() == system.read_bytes(), name
    provenance[name] = {'operation': 'trusted openEuler %%configure copy',
                        'system_path': str(system), 'system_sha256': digest(system.read_bytes())}
before = Path('packaging-notices/ltmain.sh.notice').read_bytes()
after = Path('ltmain.sh').read_bytes()
assert Path('ltmain.sh.backup').read_bytes() == before
old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
assert len(old_lines) == len(new_lines)
changes = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
assert changes
hardening = set()
for a, b in changes:
    assert a.endswith(b'compiler_flags=\n')
    prefix = a[:-len(b'compiler_flags=\n')] + b'compiler_flags="'
    assert b.startswith(prefix) and b.endswith(b'"\n')
    flags = b[len(prefix):-2]
    assert flags and b'"' not in flags and b'\n' not in flags
    assert flags in os.environ['LDFLAGS'].encode()
    hardening.add(flags)
assert len(hardening) == 1
flags = next(iter(hardening))
assert before.replace(b'compiler_flags=\n', b'compiler_flags="' + flags + b'"\n') == after
provenance['ltmain.sh'] = {'operation': 'trusted openEuler %%configure hardening substitution',
                           'original_backup_sha256': digest(before),
                           'hardening_flags': flags.decode(),
                           'full_macro_commands': 'rpmbuild-internal.log %%configure shell trace'}
build_inputs = dict(original)
for name in sorted(helpers):
    build_inputs[name] = digest(Path(name).read_bytes())
    provenance[name].update(original_sha256=original[name], postconfigure_sha256=build_inputs[name],
                            postconfigure_bytes=Path(name).stat().st_size)
Path('packaging-build-inputs.sha256').write_text(''.join(build_inputs[name] + '  ' + name + '\n' for name in original))
boundary = {'schema_version': 1, 'kind': 'sfsexp-postconfigure-build-input-boundary',
            'original_source_files': 81, 'unchanged_original_files': 78,
            'typed_helper_refreshes': provenance,
            'original_source_manifest_sha256': digest(Path('packaging-source.sha256').read_bytes()),
            'build_input_manifest_sha256': digest(Path('packaging-build-inputs.sha256').read_bytes()),
            'original_raw_notices_unchanged': True, 'upstream_source_patch': False}
Path('packaging-qa/build-input-boundary.json').write_text(json.dumps(boundary, indent=2) + '\n')
print(json.dumps(boundary, sort_keys=True))
PY_BUILD_INPUTS
sha256sum -c packaging-build-inputs.sha256
%make_build
grep -F -- '-D_NO_MEMORY_MANAGEMENT_' src/Makefile
grep -F -- '-DNODEBUG' src/Makefile
for name in bug ctest ctorture error_codes partial read_and_dump readtests vis_test; do
    test -x "tests/.libs/$name"
done
for name in binmode callbacks continuations packunpack paultest rcfile sexpvis simple_interp; do
    test -x "examples/.libs/$name"
done
sha256sum -c packaging-build-inputs.sha256

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_datadir}/sfsexp-tests
install -m0644 packaging-qa/consumer.c packaging-qa/run-qa.py packaging-qa/expected.stdout %{buildroot}%{_datadir}/sfsexp-tests/
(cd %{buildroot}%{_datadir}/sfsexp-tests && sha256sum consumer.c run-qa.py expected.stdout > SHA256SUMS)
install -d %{buildroot}%{_licensedir}/%{name}/source-notices
cp -a packaging-notices/. %{buildroot}%{_licensedir}/%{name}/source-notices/
install -m0644 COPYING LICENSE_LGPL %{SOURCE1} %{SOURCE2} packaging-qa/HELPER-LICENSE-NOTE.txt %{buildroot}%{_licensedir}/%{name}/
install -d %{buildroot}%{_docdir}/%{name}
install -m0644 README.md README_cmake.txt %{buildroot}%{_docdir}/%{name}/
# No source/example/test executable is installed; SDK libraries are upstream install.
test ! -d %{buildroot}%{_bindir}

%check
export LC_ALL=C LANG=C
make check
sha256sum -c packaging-build-inputs.sha256
python3 packaging-qa/original-oracles.py "$PWD" "$PWD/packaging-qa/original-results"
python3 packaging-qa/run-qa.py build "$PWD"
sha256sum -c packaging-build-inputs.sha256

%files
%license %{_licensedir}/%{name}
%doc %{_docdir}/%{name}
%{_libdir}/libsexp.so.1.0.0
%{_libdir}/libsexp.so.1
%{_libdir}/libsexp.so
%{_libdir}/libsexp.a
%{_libdir}/libsexp.la
%{_includedir}/sfsexp
%{_libdir}/pkgconfig/sfsexp.pc
%{_datadir}/sfsexp-tests

%changelog
* Tue Oct 27 2026 openEuler RISC-V package contributors - 1.4.1-1
- Package official release with unchanged defaults and additive SDK checks.
- Distinguish original sources from the three trusted configure-refreshed helpers.
