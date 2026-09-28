# SPDX-License-Identifier: Apache-2.0
Name:           libslz
Version:        1.3.1
Release:        1%{?dist}
Summary:        Stateless zlib-compatible compression library
License:        MIT
URL:            https://github.com/wtarreau/libslz
Source0:        libslz-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3

%description
SLZ is a low-memory stream compressor compatible with gzip, zlib, and raw
Deflate. This package includes the zenc, zdec, and zdecode utilities.

%package devel
Summary:        Development files for libslz
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header and unversioned shared-library link for SLZ applications.

%package static
Summary:        Static library for libslz
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The static SLZ library for applications requiring static linking.

%prep
%autosetup -n libslz-046706451ccc90908fd63dd2509ece96f1c18e94

%build
%make_build IGNOREGIT=1 PREFIX=%{_prefix} LIBDIR=%{_libdir} \
  USR_CFLAGS="%{optflags}" all

%install
# The upstream install-tools target copies zdecode as zdec and strips zenc
# before RPM can generate debug information. Install the already-built tools
# directly, while retaining upstream library/header installation targets.
%{__make} IGNOREGIT=1 DESTDIR=%{buildroot} PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} install-headers install-static install-shared
install -Dpm 0755 zenc %{buildroot}%{_bindir}/zenc
install -Dpm 0755 zdec %{buildroot}%{_bindir}/zdec
install -Dpm 0755 zdecode %{buildroot}%{_bindir}/zdecode

%check
# Upstream supplies fixtures but no registered check target. This downstream
# matrix exercises all levels, output formats and both input paths, then
# independently verifies decoding with SLZ and Python's zlib implementation.
task_test_dir=$(mktemp -d)
trap 'rm -rf -- "$task_test_dir"' EXIT
for fixture in tests/daniels.html tests/index.html tests/noncomp.bin; do
  for level in 0 1 2 3 4 5 6 7 8 9; do
    for format in D G Z; do
      case "$format" in
        D) wbits=-15 ;;
        G) wbits=31 ;;
        Z) wbits=15 ;;
      esac
      for input_path in direct buffered; do
        if [ "$input_path" = buffered ]; then
          ./zenc -B -"$level" -"$format" "$fixture" >"$task_test_dir/encoded"
        else
          ./zenc -"$level" -"$format" "$fixture" >"$task_test_dir/encoded"
        fi
        ./zdec -"$format" "$task_test_dir/encoded" >"$task_test_dir/decoded"
        cmp "$fixture" "$task_test_dir/decoded"
        python3 -c 'import pathlib,sys,zlib; expected=pathlib.Path(sys.argv[1]).read_bytes(); packed=pathlib.Path(sys.argv[2]).read_bytes(); actual=zlib.decompress(packed,int(sys.argv[3])); sys.exit(0 if actual==expected else 1)' \
          "$fixture" "$task_test_dir/encoded" "$wbits"
      done
    done
  done
done

%files
%license LICENSE
%doc README
%{_bindir}/zenc
%{_bindir}/zdec
%{_bindir}/zdecode
%{_libdir}/libslz.so.1

%files devel
%license LICENSE
%{_includedir}/slz.h
%{_libdir}/libslz.so

%files static
%license LICENSE
%{_libdir}/libslz.a

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Package official libslz with 180-case fixture and interoperability checks.
