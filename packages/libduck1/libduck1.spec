# SPDX-License-Identifier: LGPL-2.1-or-later
Name:           libduck1
Version:        1.1.2
Release:        1%{?dist}
Summary:        Daisy 2.02 talking book parser library
License:        LGPL-2.1-or-later
URL:            https://github.com/Skywalker13/libduck
Source0:        https://codeload.github.com/Skywalker13/libduck/tar.gz/d0ddd6bf9075199f546c5494f85512022a916a82#/libduck1-1.1.2.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/COPYING.GPL2
Source2:        https://www.gnu.org/licenses/gpl-3.0.txt#/COPYING.GPL3
BuildRequires:  gcc make libxml2-devel pkgconf which glibc-devel
BuildRequires:  binutils coreutils bash sed grep gzip tar rpm diffutils

%description
A C API for parsing Daisy 2.02 talking book metadata and navigating NCC/SMIL
chapters, paragraphs and audio URI positions. Includes the original example.

%package devel
Summary:        Development files and offline acceptance fixtures for libduck
Requires:       %{name} = %{version}-%{release}
Requires:       gcc libxml2-devel pkgconf binutils coreutils bash diffutils

%description devel
Original public header, static library, shared linker name, pkg-config metadata
and reproducible offline parser checks against the installed library.

%prep
%setup -q -n libduck-d0ddd6bf9075199f546c5494f85512022a916a82
cp -p %{SOURCE1} COPYING.GPL2
cp -p %{SOURCE2} COPYING.GPL3
mkdir -p oe-tests
cp -p src/duck.h libduck-test.c oe-tests/
(cd oe-tests && sha256sum duck.h libduck-test.c > SHA256SUMS)
cat > oe-tests/ncc.html <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<html><head><title>Offline Daisy fixture</title>
<meta name="dc:creator" content="Codex Fixture"/>
<meta name="dc:date" content="2026-10-17"/>
<meta name="dc:format" content="Daisy 2.02"/>
<meta name="dc:identifier" content="offline-duck-fixture"/>
<meta name="dc:language" content="en"/>
<meta name="dc:publisher" content="Fixture"/>
<meta name="dc:title" content="Offline Daisy fixture"/>
<meta name="ncc:charset" content="utf-8"/>
<meta name="ncc:pageFront" content="0"/>
<meta name="ncc:pageNormal" content="0"/>
<meta name="ncc:pageSpecial" content="0"/>
<meta name="ncc:tocItems" content="1"/>
<meta name="ncc:totalTime" content="00:00:02"/>
<meta name="ncc:narrator" content="Offline Narrator"/>
</head><body>
<h1 id="h1" class="title"><a href="chapter.smil#p1">Offline chapter</a></h1>
</body></html>
XML
cat > oe-tests/chapter.smil <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<smil><head>
<meta name="dc:format" content="Daisy 2.02"/>
<meta name="ncc:timeInThisSmil" content="00:00:02"/>
<meta name="ncc:totalElapsedTime" content="00:00:00"/>
</head><body><seq>
<par id="p1"><text src="text.html#t1" id="t1"/><audio src="audio.wav" clip-begin="npt=0.000s" clip-end="npt=1.000s"/></par>
<par id="p2"><text src="text.html#t2" id="t2"/><audio src="audio.wav" clip-begin="npt=1.000s" clip-end="npt=2.000s"/></par>
</seq></body></smil>
XML
cat > oe-tests/text.html <<'XML'
<html><head><title>Fixture text</title></head><body><p id="t1">First</p><p id="t2">Second</p></body></html>
XML
cat > oe-tests/expected.txt <<'TXT'
 => Offline chapter
    |- audio.wav (0.000-1.000)
    |- audio.wav (1.000-2.000)
TXT
cat > oe-tests/consumer.c <<'C'
/* Downstream offline fixture, not an upstream test suite. */
#include <duck.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static void book_s(duck_t *d, duck_book_info_t k, const char *s) {
  duck_value_t v; assert(duck_book_getinfo(d,k,&v)==0);
  assert(v.s && strcmp(v.s,s)==0); free(v.s);
}
static void smil_i(duck_t *d, duck_smilnode_info_t k, int i) {
  duck_value_t v; assert(duck_smilnode_getinfo(d,k,&v)==0); assert(v.i==i);
}
static void node_i(duck_t *d, duck_node_info_t k, int i) {
  duck_value_t v; assert(duck_node_getinfo(d,k,&v)==0); assert(v.i==i);
}
int main(int argc, char **argv) {
  duck_t *d; duck_value_t v; int s,n; assert(argc==2);
  assert(libduck_version()==LIBDUCK_VERSION_INT);
  duck_verbosity(DUCK_MSG_NONE); d=duck_init(NULL); assert(d);
  assert(duck_load(d,argv[1],DUCK_FORMAT_AUTO)==0);
  assert(duck_smilnode_number(d)==1);
  book_s(d,DUCK_BOOK_S_AUTHOR,"Codex Fixture");
  book_s(d,DUCK_BOOK_S_TITLE,"Offline Daisy fixture");
  book_s(d,DUCK_BOOK_S_NARRATOR,"Offline Narrator");
  assert(duck_book_getinfo(d,DUCK_BOOK_I_DURATION,&v)==0 && v.i==2);
  assert(duck_walk(d,1,1)==0);
  assert(duck_getpos(d,&s,&n)==0 && s==1 && n==1);
  assert(duck_smilnode_getinfo(d,DUCK_SMILNODE_S_ANCHOR,&v)==0);
  assert(v.s && strcmp(v.s,"chapter.smil")==0); free(v.s);
  assert(duck_smilnode_getinfo(d,DUCK_SMILNODE_S_HEADER,&v)==0);
  assert(v.s && strcmp(v.s,"Offline chapter")==0); free(v.s);
  smil_i(d,DUCK_SMILNODE_I_INDEX,1); smil_i(d,DUCK_SMILNODE_I_LEVEL,1);
  smil_i(d,DUCK_SMILNODE_I_TYPE,DUCK_SMILNODE_HEADING);
  smil_i(d,DUCK_SMILNODE_I_DURATION,2); smil_i(d,DUCK_SMILNODE_I_ELAPSEDTIME,0);
  assert(duck_node_getinfo(d,DUCK_NODE_S_AUDIO_URI,&v)==0);
  assert(v.s && strcmp(v.s,"audio.wav")==0); free(v.s);
  node_i(d,DUCK_NODE_I_INDEX,1); node_i(d,DUCK_NODE_I_AUDIO_POS_START,0);
  node_i(d,DUCK_NODE_I_AUDIO_POS_STOP,1000);
  assert(duck_walk(d,1,2)==0);
  assert(duck_getpos(d,&s,&n)==0 && s==1 && n==2);
  node_i(d,DUCK_NODE_I_INDEX,2); node_i(d,DUCK_NODE_I_AUDIO_POS_START,1000);
  node_i(d,DUCK_NODE_I_AUDIO_POS_STOP,2000);
  assert(duck_walk(d,1,3)!=0); assert(duck_walk(d,2,1)!=0);
  duck_uninit(d); d=duck_init(NULL); assert(d);
  assert(duck_load(d,argv[1],DUCK_FORMAT_NCX)!=0); duck_uninit(d);
  puts("PASS downstream Daisy metadata, two timed nodes, navigation and rejection");
  return 0;
}
C
cat > oe-tests/run-checks.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
tests="$root/usr/share/libduck1/tests"
lib="$root/usr/lib64"
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
cd "$tests"
sha256sum -c SHA256SUMS
cmp duck.h "$root/usr/include/duck.h"
export LD_LIBRARY_PATH="$lib"
export PKG_CONFIG_LIBDIR="$lib/pkgconfig:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$root"
test "$(pkg-config --modversion libduck)" = 1.1.2
# Recompile the unchanged original program; then replay the original installed one.
gcc -I"$root/usr/include" libduck-test.c -L"$lib" -lduck -o "$tmp/original"
"$tmp/original" "$tests/ncc.html" > "$tmp/recompiled.out"
cmp expected.txt "$tmp/recompiled.out"
"$root/usr/bin/libduck-test" "$tests/ncc.html" > "$tmp/installed.out"
cmp expected.txt "$tmp/installed.out"
gcc consumer.c $(pkg-config --cflags --libs libduck) -o "$tmp/shared"
"$tmp/shared" "$tests/ncc.html"
# libduck.pc defaults to shared metadata. Explicit static closure uses libxml2 and m.
unset PKG_CONFIG_SYSROOT_DIR
export PKG_CONFIG_LIBDIR=/usr/lib64/pkgconfig:/usr/share/pkgconfig
gcc -I"$root/usr/include" consumer.c "$lib/libduck.a" $(pkg-config --cflags --libs libxml-2.0) -lm -o "$tmp/static"
"$tmp/static" "$tests/ncc.html"
echo 'PASS downstream original-program replays=2 consumers=2 skips=0'
SH

%build
# Keep the original static/shared/apps defaults. Old arch switch needs explicit PIC.
./configure --prefix=%{_prefix} --libdir=%{_libdir} --enable-pic
grep -Fx 'BUILD_STATIC=yes' config.mak
grep -Fx 'BUILD_SHARED=yes' config.mak
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/libduck1/tests
install -m 644 oe-tests/* %{buildroot}%{_datadir}/libduck1/tests/

%check
set -eu
# No upstream check target exists. Preserve the default original program unchanged.
cmp src/duck.h oe-tests/duck.h
cmp libduck-test.c oe-tests/libduck-test.c
LD_LIBRARY_PATH="$PWD/src" ./libduck-test "$PWD/oe-tests/ncc.html" > original.out
cmp oe-tests/expected.txt original.out
bash %{buildroot}%{_datadir}/libduck1/tests/run-checks.sh %{buildroot}

%files
%license COPYING COPYING.GPL2 COPYING.GPL3
%doc AUTHORS ChangeLog README
%{_bindir}/libduck-test
%{_libdir}/libduck.so.1
%{_libdir}/libduck.so.1.1.2

%files devel
%license COPYING COPYING.GPL2 COPYING.GPL3
%{_includedir}/duck.h
%{_libdir}/libduck.so
%{_libdir}/libduck.a
%{_libdir}/pkgconfig/libduck.pc
%{_datadir}/libduck1/

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.2-1
- Retain original static/shared default build and original program.
- Add offline downstream Daisy/SMIL semantic and installed-consumer acceptance.
