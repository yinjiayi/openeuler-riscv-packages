# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}
Name:           libatomic-queue
Version:        1.9.4
Release:        1%{?dist}
Summary:        Header-only C++14 concurrent queues
License:        MIT
URL:            https://github.com/max0x7ba/atomic_queue
Source0:        atomic_queue-1.9.4.tar.gz
BuildArch:      noarch
Requires:       pkgconf
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  boost-devel
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  binutils
BuildRequires:  grep


%description
Header-only C++14 multiple-producer, multiple-consumer queues with fixed-size
circular storage and std::atomic operations. This package supplies all five
upstream public headers and architecture-independent pkg-config metadata.

%package tests
Summary:        Unmodified upstream functional tests for libatomic-queue
Requires:       %{name} = %{version}-%{release}
Requires:       gcc-c++ boost-devel pkgconf bash coreutils

%description tests
The complete original Boost.Test source, original concurrent example, their
unmodified helper header, and a downstream installed-header replay driver.
No benchmark numbers or native timing guarantees are implied.

%prep
%setup -q -n atomic_queue-40624b83b1074f34eb4dff6836740f9e2b49ad10
sha256sum include/atomic_queue/*.h src/tests.cc src/example.cc src/benchmarks.h > original.sha256
cat > run-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
prefix=${root%/}/usr
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() { rc=$?; if test "$rc" -eq 0; then rm -r -- "$work"; else printf 'Failed replay retained: %%s\n' "$work" >&2; fi; exit "$rc"; }
trap cleanup EXIT
mkdir "$work/src"
ln -s "$prefix/include" "$work/include"
cp -p "$self"/{tests.cc,example.cc,benchmarks.h} "$work/src/"
cp -p "$self/original.sha256" "$work/"
cd "$work"
sha256sum -c original.sha256
export PKG_CONFIG_SYSROOT_DIR="$root"
export PKG_CONFIG_LIBDIR="$prefix/share/pkgconfig"
unset PKG_CONFIG_PATH
test "$(pkg-config --modversion atomic_queue)" = 1.9.4
read -r -a pcflags <<< "$(pkg-config --cflags --libs atomic_queue)"
g++ -O2 -std=c++14 -pthread -DBOOST_TEST_DYN_LINK -I"$prefix/include" src/tests.cc "${pcflags[@]}" -lboost_unit_test_framework -o tests
g++ -O2 -std=c++14 -pthread -I"$prefix/include" src/example.cc "${pcflags[@]}" -o example
timeout 30m ./tests --log_level=unit_scope --report_level=short
timeout 10m ./example
printf 'PASS complete original Boost.Test and example against installed headers\n'
SH

%build
# Preserve upstream Meson defaults: tests=true, both benchmarks=false.
# There are no installed libraries; share/pkgconfig makes the payload noarch.
meson setup build --prefix=%{_prefix} --libdir=%{_datadir} --buildtype=release --wrap-mode=nodownload
meson compile -v -C build -j %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} meson install -C build --no-rebuild
install -d %{buildroot}%{_datadir}/%{name}/tests
install -pm0644 src/tests.cc src/example.cc src/benchmarks.h original.sha256 %{buildroot}%{_datadir}/%{name}/tests/
install -pm0755 run-tests.sh %{buildroot}%{_datadir}/%{name}/tests/

%check
sha256sum -c original.sha256
meson test -v -C build --no-rebuild --print-errorlogs --timeout-multiplier 120
bash %{buildroot}%{_datadir}/%{name}/tests/run-tests.sh %{buildroot}

%files
%license LICENSE
%doc README.md
%{_includedir}/atomic_queue/
%{_datadir}/pkgconfig/atomic_queue.pc

%files tests
%license LICENSE
%{_datadir}/%{name}/

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.9.4-1
- Package fixed official source with complete default tests and installed replay.
