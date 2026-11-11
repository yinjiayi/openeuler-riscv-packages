# SPDX-License-Identifier: Apache-2.0
Name:           libmsnumpress
Version:        0.2.3
Release:        1%{?dist}
Summary:        C++ numeric array compression for mass spectrometry
License:        Apache-2.0
URL:            https://github.com/ms-numpress/ms-numpress
Source0:        https://codeload.github.com/ms-numpress/ms-numpress/tar.gz/2657c2fe48ff9b5e11e87e31a7f5a16aef67bb0d#/libmsnumpress-0.2.3.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt#/APACHE-2.0.txt
BuildRequires:  gcc gcc-c++ libstdc++-devel glibc-devel make pkgconf
BuildRequires:  bash coreutils binutils rpm gzip tar grep gawk sed findutils diffutils patch

%description
The independently documented C++ component of MS Numpress compresses numeric
arrays using linear prediction, positive integer and short logged float
encodings. This package does not ship the separate Java, Python or C# bindings.
Shared/static packaging and the SONAME are downstream conventions, not an
upstream ABI stability promise.

%package devel
Summary:        Original MS Numpress C++ header and test source
Requires:       %{name} = %{version}-%{release}

%description devel
The unchanged public header, pkg-config metadata and unchanged upstream C++
test suite with an installed shared/static replay wrapper.

%package static
Summary:        Static C++ archive for MS Numpress
Requires:       %{name}-devel = %{version}-%{release}

%description static
The C++ static archive, built without removing the shared variant or tests.

%prep
%setup -q -n ms-numpress-2657c2fe48ff9b5e11e87e31a7f5a16aef67bb0d
cp -p %{SOURCE1} APACHE-2.0.txt
# No original source is edited. This wrapper is downstream packaging only.
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
cd "$work"
printf '%%s  %%s\n' 7c1b0fb26299d7e48e9ffc79c2afe51f061bfebadb4274d8403dcca99c17cb1a "$self/MSNumpressTest.cpp" | sha256sum -c -
printf '%%s  %%s\n' 399edb6f33c4f950def439d12dae5eef0d883e05335d38cddf8e3072c012a7e8 "$prefix/include/MSNumpress.hpp" | sha256sum -c -
export PKG_CONFIG_LIBDIR="$prefix/lib64/pkgconfig"
test "$(pkg-config --modversion libmsnumpress)" = 0.2.3
test "$(pkg-config --define-variable=prefix="$prefix" --variable=includedir libmsnumpress)" = "$prefix/include"
readelf -d "$prefix/lib64/libmsnumpress.so.0.2.3" | grep -F 'Library soname: [libmsnumpress.so.0]'
export LD_LIBRARY_PATH="$prefix/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
g++ -O2 -UNDEBUG -I"$prefix/include" "$self/MSNumpressTest.cpp" -L"$prefix/lib64" -lmsnumpress -o shared-test
g++ -O2 -UNDEBUG -I"$prefix/include" "$self/MSNumpressTest.cpp" "$prefix/lib64/libmsnumpress.a" -o static-test
readelf -d shared-test | grep -F 'Shared library: [libmsnumpress.so.0]'
if readelf -d static-test | grep -F 'Shared library: [libmsnumpress.so.0]'; then exit 1; fi
for linkage in shared static; do
    "./$linkage-test" > "$linkage.log" 2>&1
    cat "$linkage.log"
    test "$(grep -c '^+ pass    ' "$linkage.log")" -eq 20
    test "$(grep -c '^=== all tests succeeded! ===$' "$linkage.log")" -eq 1
    if grep -F -- '- fail    ' "$linkage.log"; then exit 1; fi
done
SH

%build
g++ %{optflags} -fPIC -c src/main/cpp/MSNumpress.cpp -o MSNumpress.o
g++ %{?__global_ldflags} -shared -Wl,--no-undefined -Wl,-soname,libmsnumpress.so.0 -o libmsnumpress.so.%{version} MSNumpress.o
ar rcs libmsnumpress.a MSNumpress.o
# Upstream has no C++ build-system file: retain its documented compile command.
(cd src/main/cpp && g++ %{optflags} -UNDEBUG MSNumpress.cpp MSNumpressTest.cpp -o test)
cat > libmsnumpress.pc <<'PC'
prefix=%{_prefix}
libdir=${prefix}/lib64
includedir=${prefix}/include

Name: libmsnumpress
Description: C++ numeric array compression for mass spectrometry
Version: %{version}
Libs: -L${libdir} -lmsnumpress
Cflags: -I${includedir}
PC

%install
install -d %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_includedir} %{buildroot}%{_datadir}/%{name}/tests
install -pm0755 libmsnumpress.so.%{version} %{buildroot}%{_libdir}/
ln -s libmsnumpress.so.%{version} %{buildroot}%{_libdir}/libmsnumpress.so.0
ln -s libmsnumpress.so.0 %{buildroot}%{_libdir}/libmsnumpress.so
install -pm0644 libmsnumpress.a %{buildroot}%{_libdir}/
install -pm0644 libmsnumpress.pc %{buildroot}%{_libdir}/pkgconfig/
install -pm0644 src/main/cpp/MSNumpress.hpp %{buildroot}%{_includedir}/
install -pm0644 src/main/cpp/MSNumpressTest.cpp %{buildroot}%{_datadir}/%{name}/tests/
install -pm0755 run-tests.sh %{buildroot}%{_datadir}/%{name}/tests/

%check
# Execute the unmodified original default main program with assertions enabled.
(cd src/main/cpp && ./test) > original-tests.log 2>&1
cat original-tests.log
test "$(grep -c '^+ pass    ' original-tests.log)" -eq 20
test "$(grep -c '^=== all tests succeeded! ===$' original-tests.log)" -eq 1
if grep -F -- '- fail    ' original-tests.log; then exit 1; fi
bash %{buildroot}%{_datadir}/%{name}/tests/run-tests.sh %{buildroot}

%files
%license APACHE-2.0.txt
%doc README.md
%{_libdir}/libmsnumpress.so.0
%{_libdir}/libmsnumpress.so.%{version}

%files devel
%license APACHE-2.0.txt
%{_includedir}/MSNumpress.hpp
%{_libdir}/libmsnumpress.so
%{_libdir}/pkgconfig/libmsnumpress.pc
%{_datadir}/%{name}/

%files static
%license APACHE-2.0.txt
%{_libdir}/libmsnumpress.a

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.2.3-1
- Package the C++ component and retain all original default C++ tests.
