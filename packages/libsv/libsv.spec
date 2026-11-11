# SPDX-License-Identifier: Apache-2.0
Name:           libsv
Version:        1.2
Release:        1%{?dist}
Summary:        Public-domain C99 semantic version parsing and comparison library
License:        Unlicense
URL:            https://github.com/uael/sv
Source0:        libsv-1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  cmake >= 3.25
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
%description
Public-domain C99 semantic version parsing and comparison library

%package devel
Summary:        Headers and original test sources for libsv
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       pkgconf

%description devel
Development headers, pkg-config metadata and the seven unmodified upstream
test sources for checking the installed semantic version library.

%prep
%autosetup -n sv-3dfbda36428a7631025aaa0acef41e681824e9d1 -p1
cat > test/SHA256SUMS <<'HASHES'
2a7020c581c581b2c402a949acd07e6964d6bc262359bcbaf470eddde8424f02  comp.c
8045f9a685b6f18ef080bdc6b159d64d234bb446d973a8a5ccc475fca79cdc2d  match.c
71158e25dbbbdfbe03f524386ef1a31ba35ca00a6cd228e5e486a75e67c8066f  range.c
29ea2048e582d09d18061e61c9fe3552e3ae3ed68e43e29e76ad545c1b6b61dd  semvers.c
7a65328e4d3cff39ac9d2fa8bc403f1e73b5499c025b560048cb7764569bfcd3  usage.c
d350979c187bffb99d222b6d302edfcd362db5af43542c2473056045acad3532  utils.c
7f49307a96fa50ad65c656bbf47342fe12f43bc01a682c9297168d05dcb80983  version.c
HASHES
(cd test && sha256sum -c SHA256SUMS)

%build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags} -UNDEBUG" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} -DCMAKE_INSTALL_INCLUDEDIR=include
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libsv/tests
install -m 0644 test/*.c test/SHA256SUMS %{buildroot}%{_datadir}/libsv/tests/

%check
ctest --test-dir build --verbose --output-on-failure --no-tests=error
ctest --test-dir build --show-only | grep -F 'Total Tests: 7'
(cd test && sha256sum -c SHA256SUMS)
mkdir staged-tests
for name in version comp match range semvers utils usage; do
    gcc %{optflags} -UNDEBUG -std=c99 -I%{buildroot}%{_includedir}/sv \
        test/$name.c -L%{buildroot}%{_libdir} -lsv -o staged-tests/$name
    (cd staged-tests && env LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./$name)
    echo "PASS original-staged $name"
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license UNLICENSE
%doc README.md
%{_libdir}/libsv.so.1*

%files devel
%{_includedir}/sv/
%{_libdir}/libsv.so
%{_libdir}/pkgconfig/libsv.pc
%{_datadir}/libsv/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Pin the official release and retain all seven original tests with assertions.
