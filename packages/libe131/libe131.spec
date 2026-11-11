# SPDX-License-Identifier: Apache-2.0
Name:           libe131
Version:        1.4.0
Release:        1%{?dist}
Summary:        Lightweight E1.31 sACN packet and communication library
License:        Apache-2.0 AND X11 AND FSFAP AND FSFUL AND GPL-3.0-or-later AND LicenseRef-Shelby-Merrick-E131
URL:            https://github.com/hhromic/libe131
Source0:        libe131-1.4.0.tar.gz
Source1:        GPL-2.0.txt
Source2:        GPL-3.0.txt
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
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       findutils
Requires:       gawk
Requires:       gcc
Requires:       glibc-devel
Requires:       grep

%description
Libe131 provides packet, destination and UDP communication APIs for the
E1.31 sACN lighting protocol. Original shared/static libraries, header,
libtool archive and documentation are retained. Added packet/address QA
is not a live lighting, network-performance or security certification.

%prep
%setup -q -n libe131-1.4.0
find . -type f -print | LC_ALL=C sort > ../libe131-original-files.list
test "$(wc -l < ../libe131-original-files.list)" -eq 23
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    destination="source-notices/$rel.notice"
    install -d "${destination%/*}"
    cp -p "$item" "$destination"
    chmod 0644 "$destination"
done < ../libe131-original-files.list
(cd source-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../libe131-notice-SHA256SUMS
mv ../libe131-notice-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 23
cp -p %{SOURCE1} GPL-2.0.txt
cp -p %{SOURCE2} GPL-3.0.txt
cat > Shelby-Merrick-E131.h.notice <<'SHELBY_NOTICE'
/*
* E131.h
*
* Project: E131 - E.131 (sACN) library for Arduino
* Copyright (c) 2015 Shelby Merrick
* http://www.forkineye.com
*
*  This program is provided free for you to use in any way that you wish,
*  subject to the laws and regulations where you are using it.  Due diligence
*  is strongly suggested before using this code.  Please give credit where due.
*
*  The Author makes no warranty of any kind, express or implied, with regard
*  to this program or the documentation contained in this document.  The
*  Author shall not be liable in any event for incidental or consequential
*  damages in connection with, or arising out of, the furnishing, performance
*  or use of these programs.
*
*/
SHELBY_NOTICE
cat > Shelby-Merrick-E131.cpp.notice <<'SHELBY_NOTICE'
/*
* E131.cpp
*
* Project: E131 - E.131 (sACN) library for Arduino
* Copyright (c) 2015 Shelby Merrick
* http://www.forkineye.com
*
*  This program is provided free for you to use in any way that you wish,
*  subject to the laws and regulations where you are using it.  Due diligence
*  is strongly suggested before using this code.  Please give credit where due.
*
*  The Author makes no warranty of any kind, express or implied, with regard
*  to this program or the documentation contained in this document.  The
*  Author shall not be liable in any event for incidental or consequential
*  damages in connection with, or arising out of, the furnishing, performance
*  or use of these programs.
*
*/
SHELBY_NOTICE
cat > api-smoke.c <<'C'
/* Copyright 2026 openEuler RISC-V package contributors
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * https://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. Full Apache text ships in original LICENSE.
 */
#include <assert.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <e131.h>

static int (*volatile init_fn)(e131_packet_t *,uint16_t,uint16_t)=e131_pkt_init;
static e131_error_t (*volatile validate_fn)(const e131_packet_t *)=e131_pkt_validate;
static bool (*volatile get_fn)(const e131_packet_t *,e131_option_t)=e131_get_option;
static int (*volatile set_fn)(e131_packet_t *,e131_option_t,bool)=e131_set_option;
static int (*volatile multicast_fn)(e131_addr_t *,uint16_t,uint16_t)=e131_multicast_dest;
static int (*volatile dest_fn)(char *,const e131_addr_t *)=e131_dest_str;
static bool (*volatile discard_fn)(const e131_packet_t *,uint8_t)=e131_pkt_discard;
static int (*volatile dump_fn)(FILE *,const e131_packet_t *)=e131_pkt_dump;
static const char *(*volatile error_fn)(e131_error_t)=e131_strerror;

int main(void) {
    e131_packet_t p,q;
    _Static_assert(sizeof(e131_packet_t)==638,"wire packet width");
    assert(init_fn(&p,1,24)==0);
    assert(E131_DEFAULT_PORT==5568 && E131_DEFAULT_PRIORITY==100);
    assert(ntohs(p.root.preamble_size)==16 && p.root.postamble_size==0);
    assert(ntohs(p.root.flength)==0x7086 && ntohl(p.root.vector)==4);
    static const uint8_t acn[12]={0x41,0x53,0x43,0x2d,0x45,0x31,0x2e,0x31,0x37,0,0,0};
    assert(!memcmp(p.root.acn_pid,acn,sizeof acn));
    assert(ntohs(p.frame.flength)==0x7070 && ntohl(p.frame.vector)==2);
    assert(p.frame.priority==100 && ntohs(p.frame.universe)==1);
    assert(ntohs(p.dmp.flength)==0x7023 && ntohs(p.dmp.prop_val_cnt)==25);
    assert(p.dmp.vector==2 && p.dmp.type==0xa1 && p.dmp.first_addr==0 && ntohs(p.dmp.addr_inc)==1);
    assert(init_fn(&q,63999,512)==0 && ntohs(q.dmp.prop_val_cnt)==513);
    q=p;errno=0;assert(init_fn(&q,0,24)==-1 && errno==EINVAL && !memcmp(&q,&p,sizeof p));
    errno=0;assert(init_fn(&q,64000,24)==-1 && errno==EINVAL);
    errno=0;assert(init_fn(&q,1,0)==-1 && errno==EINVAL);
    errno=0;assert(init_fn(&q,1,513)==-1 && errno==EINVAL);
    errno=0;assert(init_fn(NULL,1,24)==-1 && errno==EINVAL);
    puts("case 1 packet wire layout and initialization boundaries PASS");

    assert(validate_fn(&p)==E131_ERR_NONE && validate_fn(NULL)==E131_ERR_NULLPTR);
    q=p;q.root.preamble_size=htons(17);assert(validate_fn(&q)==E131_ERR_PREAMBLE_SIZE);
    q=p;q.root.postamble_size=htons(1);assert(validate_fn(&q)==E131_ERR_POSTAMBLE_SIZE);
    q=p;q.root.acn_pid[0]^=1;assert(validate_fn(&q)==E131_ERR_ACN_PID);
    q=p;q.root.vector=htonl(5);assert(validate_fn(&q)==E131_ERR_VECTOR_ROOT);
    q=p;q.frame.vector=htonl(3);assert(validate_fn(&q)==E131_ERR_VECTOR_FRAME);
    q=p;q.dmp.vector=3;assert(validate_fn(&q)==E131_ERR_VECTOR_DMP);
    q=p;q.dmp.type=0xa0;assert(validate_fn(&q)==E131_ERR_TYPE_DMP);
    q=p;q.dmp.first_addr=htons(1);assert(validate_fn(&q)==E131_ERR_FIRST_ADDR_DMP);
    q=p;q.dmp.addr_inc=htons(2);assert(validate_fn(&q)==E131_ERR_ADDR_INC_DMP);
    assert(!strcmp(error_fn(E131_ERR_NONE),"Success"));
    assert(!strcmp(error_fn(E131_ERR_PREAMBLE_SIZE),"Invalid Preamble Size"));
    assert(!strcmp(error_fn(E131_ERR_ADDR_INC_DMP),"Invalid DMP Address Increment"));
    assert(!strcmp(error_fn(E131_ERR_NULLPTR),"Unknown error"));
    assert(!strcmp(error_fn((e131_error_t)999),"Unknown error"));
    puts("case 2 validator mutations and exact error strings PASS");

    q=p;q.frame.options=3;
    assert(!get_fn(&q,E131_OPT_TERMINATED) && !get_fn(&q,E131_OPT_PREVIEW));
    assert(set_fn(&q,E131_OPT_TERMINATED,true)==0 && q.frame.options==0x43);
    assert(get_fn(&q,E131_OPT_TERMINATED) && !get_fn(&q,E131_OPT_PREVIEW));
    assert(set_fn(&q,E131_OPT_PREVIEW,true)==0 && q.frame.options==0xc3);
    assert(set_fn(&q,E131_OPT_TERMINATED,false)==0 && q.frame.options==0x83);
    assert(!get_fn(&q,E131_OPT_TERMINATED) && get_fn(&q,E131_OPT_PREVIEW));
    assert(!get_fn(NULL,E131_OPT_PREVIEW));errno=0;
    assert(set_fn(NULL,E131_OPT_PREVIEW,true)==-1 && errno==EINVAL);
    puts("case 3 independent framing options and null behavior PASS");

    e131_addr_t dest;char address[32];
    assert(multicast_fn(&dest,1,5568)==0 && dest.sin_family==AF_INET && ntohs(dest.sin_port)==5568);
    assert(dest_fn(address,&dest)==0 && !strcmp(address,"239.255.0.1:5568"));
    assert(multicast_fn(&dest,63999,65535)==0 && dest_fn(address,&dest)==0);
    assert(!strcmp(address,"239.255.249.255:65535"));
    errno=0;assert(multicast_fn(&dest,0,5568)==-1 && errno==EINVAL);
    errno=0;assert(multicast_fn(&dest,64000,5568)==-1 && errno==EINVAL);
    errno=0;assert(multicast_fn(NULL,1,5568)==-1 && errno==EINVAL);
    errno=0;assert(dest_fn(NULL,&dest)==-1 && errno==EINVAL);
    errno=0;assert(dest_fn(address,NULL)==-1 && errno==EINVAL);
    puts("case 4 pure multicast address formatting and errors PASS");

    q=p;q.frame.seq_number=100;assert(discard_fn(&q,100));
    q.frame.seq_number=99;assert(discard_fn(&q,100));
    q.frame.seq_number=81;assert(discard_fn(&q,100));
    q.frame.seq_number=80;assert(!discard_fn(&q,100));
    q.frame.seq_number=101;assert(!discard_fn(&q,100));
    q.frame.seq_number=0;assert(!discard_fn(&q,255));
    q.frame.seq_number=255;assert(discard_fn(&q,0));
    assert(discard_fn(NULL,0));
    puts("case 5 sequence duplicate window and wrap behavior PASS");

    FILE *stream=tmpfile();assert(stream!=NULL);
    assert(dump_fn(stream,&p)==0 && fflush(stream)==0);
    long length=ftell(stream);assert(length>0 && length<4096);
    assert(fseek(stream,0,SEEK_SET)==0);char output[4096];
    assert(fread(output,1,(size_t)length,stream)==(size_t)length);
    output[length]='\0';assert(!ferror(stream));
    assert(strstr(output,"[Root Layer]\n") && strstr(output,"[Framing Layer]\n"));
    assert(strstr(output,"[Device Management Protocol (DMP) Layer]\n") && strstr(output,"[DMP Property Values]\n"));
    assert(strstr(output,"Property Value Count ... 25\n"));
    errno=0;assert(dump_fn(NULL,&p)==-1 && errno==EINVAL);
    errno=0;assert(dump_fn(stream,NULL)==-1 && errno==EINVAL);
    assert(fclose(stream)==0);
    puts("case 6 initialized packet stream dump and null errors PASS");
    puts("libe131 six cases PASS");
    return 0;
}
C
cat > expected.stdout <<'EXPECTED'
case 1 packet wire layout and initialization boundaries PASS
case 2 validator mutations and exact error strings PASS
case 3 independent framing options and null behavior PASS
case 4 pure multicast address formatting and errors PASS
case 5 sequence duplicate window and wrap behavior PASS
case 6 initialized packet stream dump and null errors PASS
libe131 six cases PASS
EXPECTED

%build
%configure --enable-shared --enable-static --docdir=%{_docdir}/%{name} CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"
%make_build
gcc %{optflags} -std=gnu11 -Wall -Wextra -Werror -UNDEBUG -Isrc api-smoke.c -L.libs -le131 %{?build_ldflags} -o api-smoke

%install
%make_install
install -d %{buildroot}%{_datadir}/libe131-tests
install -m 0644 api-smoke.c expected.stdout %{buildroot}%{_datadir}/libe131-tests/

%check
export LC_ALL=C
if make check > upstream-check.log 2>&1; then cat upstream-check.log; else
    status=$?; cat upstream-check.log >&2; exit "$status"
fi
# Original check-am only builds all-am: zero registered functional cases.
if LD_LIBRARY_PATH="$PWD/.libs" ./api-smoke > api.stdout 2> api.stderr; then :; else
    status=$?; cat api.stdout api.stderr >&2; exit "$status"
fi
cmp expected.stdout api.stdout
test ! -s api.stderr
cat api.stdout
# Install-post stripping precedes this phase; bind actual installed bytes.
(cd %{buildroot}; sha256sum usr/lib64/libe131.so.1.0.4 usr/lib64/libe131.a usr/lib64/libe131.la usr/include/e131.h usr/share/libe131-tests/api-smoke.c usr/share/libe131-tests/expected.stdout) > %{buildroot}%{_datadir}/libe131-tests/SHA256SUMS

%files
%license LICENSE GPL-2.0.txt GPL-3.0.txt Shelby-Merrick-E131.h.notice Shelby-Merrick-E131.cpp.notice source-notices
%doc %{_docdir}/%{name}/
%{_libdir}/libe131.so.1.0.4
%{_libdir}/libe131.so.1
%{_libdir}/libe131.so
%{_libdir}/libe131.a
%{_libdir}/libe131.la
%{_includedir}/e131.h
%{_datadir}/libe131-tests/

%changelog
* Mon Oct 26 2026 openEuler RISC-V package contributors - 1.4.0-1
- Package official fixed release with original shared/static build and check.
- Preserve all original and attributed notices; add six strict API cases.
