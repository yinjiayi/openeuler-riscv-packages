# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 3cc5c8a72599aed37efcb1343dbfb3630d7d3ce3
Name:           libdontdie
Version:        1.2.0
Release:        1%{?dist}
Summary:        TCP keepalive socket interposition library
License:        MIT AND BSD-3-Clause
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
%license LICENSE COPYING.Java
%doc README.md doc/Contributors.txt .travis.yml
%{_libdir}/libdontdie.so
%{_libdir}/libdontdie.so.0
%{_mandir}/man7/libdontdie.7*
%{_datadir}/libdontdie/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Package fixed official source; preserve all original all/testapps targets.
