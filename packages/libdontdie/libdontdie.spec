# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 3cc5c8a72599aed37efcb1343dbfb3630d7d3ce3
Name:           libdontdie
Version:        1.2.0
Release:        1%{?dist}
Summary:        TCP keepalive socket interposition library
License:        MIT AND BSD-3-Clause AND Apache-2.0
URL:            https://github.com/flonatel/libdontdie
Source0:        libdontdie-1.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  java-17-openjdk-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
Requires:       gcc
Requires:       glibc-devel
Requires:       java-17-openjdk-devel
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       rpm

%description
LD_PRELOAD library that enables TCP keepalive on newly created Internet
stream sockets and optionally sets their idle, interval and probe counts.
Includes the unchanged upstream C and Java manual test applications and a
separately labeled downstream socket-option functional check. No privileged
packet-loss, keepalive timing, performance or native-hardware claim is made.

%prep
%setup -q -n libdontdie-%{upstream_commit}
# Retain Oracle/Andreas BSD-3-Clause notice and disclaimer in binary RPM too.
cp -p test/java/EchoClient.java COPYING.Java
# Downstream contracts are Apache-2.0; embed the full repository license so
# the source RPM is self-contained and the binary RPM carries its terms.
cat > COPYING.Apache-2.0 <<'APACHE_LICENSE'
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
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
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
APACHE_LICENSE
mkdir contract
cat > contract/check-options.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void need(int ok, const char *what) {
    if (!ok) { perror(what); exit(1); }
}
static void option(int fd, int level, int name, int expected) {
    int value=-1; socklen_t len=sizeof value;
    need(getsockopt(fd,level,name,&value,&len)==0,"getsockopt");
    if (len!=sizeof value || value!=expected) {
        fprintf(stderr,"option %d: expected %d, got %d\n",name,expected,value);
        exit(1);
    }
}
int main(int argc, char **argv) {
    need(argc==2,"mode");
    int on=strcmp(argv[1],"disabled")!=0;
    int custom=strcmp(argv[1],"custom")==0;
    int fd=socket(AF_INET,SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK,0);
    need(fd>=0,"IPv4 stream socket"); option(fd,SOL_SOCKET,SO_KEEPALIVE,on);
    need((fcntl(fd,F_GETFD)&FD_CLOEXEC)!=0,"CLOEXEC preserved");
    need((fcntl(fd,F_GETFL)&O_NONBLOCK)!=0,"NONBLOCK preserved");
    if (custom) {
        option(fd,SOL_TCP,TCP_KEEPIDLE,7);
        option(fd,SOL_TCP,TCP_KEEPINTVL,3);
        option(fd,SOL_TCP,TCP_KEEPCNT,4);
    }
    need(close(fd)==0,"close");
    fd=socket(AF_INET6,SOCK_STREAM,0); need(fd>=0,"IPv6 stream socket");
    option(fd,SOL_SOCKET,SO_KEEPALIVE,on); need(close(fd)==0,"close IPv6");
    fd=socket(AF_INET,SOCK_DGRAM,0); need(fd>=0,"datagram socket");
    option(fd,SOL_SOCKET,SO_KEEPALIVE,0); need(close(fd)==0,"close datagram");
    fd=socket(AF_UNIX,SOCK_STREAM,0); need(fd>=0,"Unix socket");
    option(fd,SOL_SOCKET,SO_KEEPALIVE,0); need(close(fd)==0,"close Unix");
    errno=0; fd=socket(-1,SOCK_STREAM,0);
    need(fd==-1 && errno==EAFNOSUPPORT,"invalid family error preserved");
    printf("PASS downstream socket-option mode=%s\n",argv[1]);
    return 0;
}
C
cat > contract/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
prefix="${root%/}/usr"
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() {
    rc=$?
    if test "$rc" -eq 0; then rm -rf -- "$work"; else printf 'FAIL evidence retained: %s\n' "$work" >&2; fi
    exit "$rc"
}
trap cleanup EXIT
cd "$self"
sha256sum -c SHA256SUMS
readelf -d "$prefix/lib64/libdontdie.so" > "$work/dynamic"
grep -F 'Library soname: [libdontdie.so.0]' "$work/dynamic"
test "$(readlink "$prefix/lib64/libdontdie.so.0")" = libdontdie.so
unset LD_PRELOAD DD_DEBUG DD_USE_KEEPALIVE DD_EVAL_ENVIRONMENT_ONCE
unset DD_TCP_KEEPALIVE_TIME DD_TCP_KEEPALIVE_INTVL DD_TCP_KEEPALIVE_PROBES
gcc -O2 -g -UNDEBUG -Wall -Wextra "$self/check-options.c" -o "$work/check-options"
timeout 30s "$work/check-options" disabled
env LD_PRELOAD="$prefix/lib64/libdontdie.so" timeout 30s "$work/check-options" default
env LD_PRELOAD="$prefix/lib64/libdontdie.so" DD_USE_KEEPALIVE=0 timeout 30s "$work/check-options" disabled
env LD_PRELOAD="$prefix/lib64/libdontdie.so" DD_TCP_KEEPALIVE_TIME=7 \
    DD_TCP_KEEPALIVE_INTVL=3 DD_TCP_KEEPALIVE_PROBES=4 timeout 30s "$work/check-options" custom
# The original manual programs have no automated upstream suite. These are
# bounded interface/exit checks, not their privileged network/timing scenario.
printf 'p\n' > "$work/ping"
printf 'pong\n' > "$work/expected"
for name in tcp_server tcp_client; do
    timeout 30s "$self/upstream/Cblackbox/$name" < "$work/ping" > "$work/$name.out"
    cmp "$work/expected" "$work/$name.out"
done
# One original socket/close iteration, without timing or a benchmark claim.
env LD_PRELOAD="$prefix/lib64/libdontdie.so" timeout 30s "$self/upstream/Cperformance/perf" 1
set +e
timeout 30s java -cp "$self/upstream/java" EchoClient > "$work/java.out" 2> "$work/java.err"
rc=$?
set -e
test "$rc" -eq 1
grep -Fx 'Usage: java EchoClient <host name> <port number>' "$work/java.err"
echo 'PASS original testapps built=4 bounded interfaces=4 downstream socket-option modes=4; native timing not tested'
SH
chmod 0755 contract/run-contract.sh

%build
# Environment flags preserve all upstream additions, including -fpic/-Wall/-O3.
export CFLAGS="%{optflags} -g -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
# Exactly the original .travis.yml targets, without changing their recipes.
make %{?_smp_mflags} all
make %{?_smp_mflags} testapps

%install
# Upstream supplies no install target; preserve its SONAME and symlink layout.
install -d %{buildroot}%{_libdir} %{buildroot}%{_mandir}/man7
install -m 0755 libdontdie.so %{buildroot}%{_libdir}/libdontdie.so
ln -s libdontdie.so %{buildroot}%{_libdir}/libdontdie.so.0
install -m 0644 doc/man/libdontdie.7 %{buildroot}%{_mandir}/man7/
testdir=%{buildroot}%{_datadir}/libdontdie/tests
install -d "$testdir/upstream/Cblackbox" "$testdir/upstream/Cperformance" "$testdir/upstream/java"
cp -p contract/* "$testdir/"
cp -p test/Cblackbox/tcp_server test/Cblackbox/tcp_client test/Cblackbox/*.c "$testdir/upstream/Cblackbox/"
cp -p test/Cperformance/perf test/Cperformance/perf.c "$testdir/upstream/Cperformance/"
cp -p test/java/EchoClient.java test/java/EchoClient.class "$testdir/upstream/java/"
(cd "$testdir" && sha256sum check-options.c upstream/Cblackbox/*.c upstream/Cperformance/perf.c upstream/java/EchoClient.java > SHA256SUMS)

%check
bash %{buildroot}%{_datadir}/libdontdie/tests/run-contract.sh %{buildroot}

%files
%license LICENSE COPYING.Java COPYING.Apache-2.0
%doc README.md doc/Contributors.txt .travis.yml
%{_libdir}/libdontdie.so
%{_libdir}/libdontdie.so.0
%{_mandir}/man7/libdontdie.7*
%{_datadir}/libdontdie/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Package fixed official source; preserve all original all/testapps targets.
