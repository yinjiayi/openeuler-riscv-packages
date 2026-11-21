# SPDX-License-Identifier: MIT
Name:           libsquish
Version:        1.15
Release:        1%{?dist}
Summary:        DXT texture compression library
License:        MIT
URL:            https://sourceforge.net/projects/libsquish/
Source0:        https://downloads.sourceforge.net/project/libsquish/libsquish-%{version}.tgz
Patch0:         0001-default-sse2-only-on-x86.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libgomp
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils

%description
Libsquish compresses and decompresses DXT texture blocks and images.
The original default static and OpenMP-enabled build is retained; a separate
shared build supplies runtime consumers and installed functional validation.

%package devel
Summary:        Headers and static development library for libsquish
Requires:       %{name} = %{version}-%{release}

%description devel
The public C++ header, linker symlink, and original default static library.

%prep
# The official archive has no enclosing source directory.
%setup -q -c -n %{name}-%{version}
# Preserve every original member before any package patch/build generation.
mkdir license-notices
find . -type f ! -path './license-notices/*' -print | LC_ALL=C sort > ../libsquish-original-members.list
test "$(wc -l < ../libsquish-original-members.list)" -eq 54
while IFS= read -r path; do
    relative=${path#./}
    mkdir -p "license-notices/$(dirname "$relative")"
    cp -p "$path" "license-notices/$relative.notice"
done < ../libsquish-original-members.list
rm ../libsquish-original-members.list
(
    cd license-notices
    find . -type f -name '*.notice' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
test "$(wc -l < license-notices/SHA256SUMS)" -eq 54
%autopatch -p1
cat > api-smoke.cpp <<'API_EOF'
// SPDX-License-Identifier: MIT
// Package-added functional checks; not an upstream test or quality benchmark.
#include <squish.h>
#include <cassert>
#include <cstdio>
#include <cstring>

using squish::u8;

static void black(u8 *p, int pixels, bool alpha_pattern = false)
{
    for (int i = 0; i < pixels; ++i) {
        p[4*i] = p[4*i+1] = p[4*i+2] = 0;
        p[4*i+3] = alpha_pattern && !(i & 1) ? 0 : 255;
    }
}

static void assert_black(const u8 *p, int pixels, bool alpha_pattern = false)
{
    for (int i = 0; i < pixels; ++i) {
        assert(p[4*i] == 0 && p[4*i+1] == 0 && p[4*i+2] == 0);
        assert(p[4*i+3] == (alpha_pattern && !(i & 1) ? 0 : 255));
    }
}

int main()
{
    // 1: Documented positive dimensions, including partial edge blocks.
    assert(squish::GetStorageRequirements(4, 4, squish::kDxt1) == 8);
    assert(squish::GetStorageRequirements(5, 5, squish::kDxt1) == 32);
    assert(squish::GetStorageRequirements(5, 5, squish::kDxt3) == 64);
    assert(squish::GetStorageRequirements(5, 5, squish::kDxt5) == 64);
    std::puts("case 1 storage dimensions PASS");

    u8 rgba[64], decoded[64], block[16];
    black(rgba, 16);
    // 2: Exactly representable black, default cluster fit, complete valid mask.
    squish::CompressMasked(rgba, 0xffff, block, squish::kDxt1);
    squish::Decompress(decoded, block, squish::kDxt1);
    assert_black(decoded, 16);
    std::puts("case 2 DXT1 exact black PASS");

    // 3 and 4: Exactly representable alpha endpoints, not a lossy-quality bound.
    black(rgba, 16, true);
    squish::CompressMasked(rgba, 0xffff, block, squish::kDxt3);
    squish::Decompress(decoded, block, squish::kDxt3);
    assert_black(decoded, 16, true);
    std::puts("case 3 DXT3 alpha endpoints PASS");
    squish::CompressMasked(rgba, 0xffff, block, squish::kDxt5);
    squish::Decompress(decoded, block, squish::kDxt5);
    assert_black(decoded, 16, true);
    std::puts("case 4 DXT5 alpha endpoints PASS");

    // 5: Nonmultiple dimensions exercise original partial-block mask/OpenMP path.
    u8 image[100], output[102], packed[66];
    black(image, 25);
    std::memset(output, 0xa7, sizeof output);
    std::memset(packed, 0xb9, sizeof packed);
    squish::CompressImage(image, 5, 5, 20, packed+1, squish::kDxt5);
    assert(packed[0] == 0xb9 && packed[65] == 0xb9);
    squish::DecompressImage(output+1, 5, 5, 20, packed+1, squish::kDxt5);
    assert(output[0] == 0xa7 && output[101] == 0xa7);
    assert_black(output+1, 25);
    double colour_error = -1, alpha_error = -1;
    squish::ComputeMSE(image, 5, 5, 20, packed+1, squish::kDxt5,
                       colour_error, alpha_error);
    assert(colour_error == 0 && alpha_error == 0);
    std::puts("case 5 partial image canaries and exact MSE PASS");

    // 6: Independently specified DXT1 blocks, not merely encoder/decoder agreement.
    const u8 known_opaque[8] = {0,0,0,0,0,0,0,0};
    squish::Decompress(decoded, known_opaque, squish::kDxt1);
    assert_black(decoded, 16);
    const u8 known_transparent[8] = {0,0,0,0,255,255,255,255};
    squish::Decompress(decoded, known_transparent, squish::kDxt1);
    for (int i = 0; i < 64; ++i) assert(decoded[i] == 0);
    std::puts("case 6 independent DXT1 wire blocks PASS");
    std::puts("libsquish six package API cases PASS");
}
API_EOF

%build
# Original preferred CMake default: static ON, OpenMP ON, Altivec/extras OFF.
cmake -S . -B build-default -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_C_FLAGS='%{optflags}' \
    -DCMAKE_CXX_FLAGS='%{optflags}'
grep -Fx 'BUILD_SHARED_LIBS:BOOL=OFF' build-default/CMakeCache.txt
grep -Fx 'BUILD_SQUISH_WITH_OPENMP:BOOL=ON' build-default/CMakeCache.txt
grep -Fx 'BUILD_SQUISH_WITH_SSE2:BOOL=OFF' build-default/CMakeCache.txt
grep -Fx 'BUILD_SQUISH_WITH_ALTIVEC:BOOL=OFF' build-default/CMakeCache.txt
grep -Fx 'BUILD_SQUISH_EXTRA:BOOL=OFF' build-default/CMakeCache.txt
grep -F -- '-DSQUISH_USE_OPENMP' build-default/CMakeFiles/squish.dir/flags.make
cmake --build build-default --parallel %{?_smp_build_ncpus}
# Add a distinct shared build; do not replace the default static build above.
cmake -S . -B build-shared -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_C_FLAGS='%{optflags}' \
    -DCMAKE_CXX_FLAGS='%{optflags}' -DBUILD_SHARED_LIBS=ON
grep -Fx 'BUILD_SQUISH_WITH_OPENMP:BOOL=ON' build-shared/CMakeCache.txt
grep -F -- '-DSQUISH_USE_OPENMP' build-shared/CMakeFiles/squish.dir/flags.make
cmake --build build-shared --parallel %{?_smp_build_ncpus}
g++ %{optflags} -UNDEBUG -I. api-smoke.cpp build-default/libsquish.a \
    -fopenmp -o api-static-smoke
g++ %{optflags} -UNDEBUG -I. api-smoke.cpp -Lbuild-shared -lsquish \
    -o api-smoke

%install
DESTDIR=%{buildroot} cmake --install build-default
DESTDIR=%{buildroot} cmake --install build-shared
# The original CMake install set uses literal lib. Preserve the whole set,
# relocating to the target's lib64 packaging path without changing features.
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/libsquish* %{buildroot}%{_libdir}/
rmdir %{buildroot}%{_prefix}/lib
install -d %{buildroot}%{_libexecdir}/libsquish-tests
install -m 0755 api-smoke %{buildroot}%{_libexecdir}/libsquish-tests/api-smoke
install -m 0644 api-smoke.cpp %{buildroot}%{_libexecdir}/libsquish-tests/api-smoke.cpp

%check
(
    cd license-notices
    sha256sum -c SHA256SUMS
)
# Upstream registers no default runtime test cases. These are package additions.
./api-static-smoke
LD_LIBRARY_PATH="$PWD/build-shared" ./api-smoke
# %check follows buildroot post-processing: bind installed post-strip bytes.
(
    cd %{buildroot}%{_libexecdir}/libsquish-tests
    sha256sum api-smoke api-smoke.cpp > SHA256SUMS
)

%files
%license LICENSE.txt license-notices
%doc README.txt ChangeLog.txt
%{_libdir}/libsquish.so.0.0
%{_libexecdir}/libsquish-tests/

%files devel
%{_includedir}/squish.h
%{_libdir}/libsquish.so
%{_libdir}/libsquish.a

%changelog
* Sat Oct 24 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 1.15-1
- Preserve static/OpenMP defaults and select existing scalar backend on non-x86.
- Add separate shared variant and strict default-static/installed API checks.
