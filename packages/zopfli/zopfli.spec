# SPDX-License-Identifier: Apache-2.0
Name:           zopfli
Version:        1.0.3
Release:        3%{?dist}
Summary:        High-density DEFLATE and PNG compression tools
License:        Apache-2.0
URL:            https://github.com/google/zopfli
Source0:        zopfli-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  golang
BuildRequires:  make

%description
Zopfli is a compression suite that produces standards-compatible DEFLATE,
gzip, zlib, and PNG streams while optimizing for compressed size.

%prep
%autosetup -n zopfli-bd64b2f0553d4f1ef4e6627647c5d9fc8c71ffc0 -p1

%build
%set_build_flags
%make_build \
  CC="%{__cc}" \
  CXX="%{__cxx}" \
  CFLAGS="%{build_cflags}" \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags}"

%install
install -Dpm0755 zopfli %{buildroot}%{_bindir}/zopfli
install -Dpm0755 zopflipng %{buildroot}%{_bindir}/zopflipng

%check
# The release archive ships two Go/CGO test packages. Link them to the just
# built C and C++ libraries and prohibit module/network resolution.
ln -s libzopfli.so.1.0.3 libzopfli.so
ln -s libzopfli.so.1.0.3 libzopfli.so.1
ln -s libzopflipng.so.1.0.3 libzopflipng.so
ln -s libzopflipng.so.1.0.3 libzopflipng.so.1
export CGO_CFLAGS="%{build_cflags} -I$PWD/src/zopfli -I$PWD/src/zopflipng"
export CGO_LDFLAGS="%{build_ldflags} -L$PWD"
export LD_LIBRARY_PATH="$PWD"
export GO111MODULE=off
export GOPROXY=off
export GOSUMDB=off
export GOCACHE="$PWD/.gocache"
go test -count=1 -v ./go/zopfli ./go/zopflipng

%files
%license COPYING
%doc CONTRIBUTORS README README.zopflipng
%{_bindir}/zopfli
%{_bindir}/zopflipng

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-3
- Rebuild the canonical tool package with both complete upstream test suites.
