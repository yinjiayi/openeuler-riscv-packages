# SPDX-License-Identifier: Apache-2.0
Name:           miniz
Version:        3.1.2
Release:        1%{?dist}
Summary:        Lossless compression library implementing zlib and Deflate
License:        MIT AND Unlicense
URL:            https://github.com/richgel999/miniz
Source0:        miniz-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconf

%description
Miniz is a compact C library implementing zlib, Deflate, ZIP archive, and
simple PNG writing APIs without depending on zlib.

%package devel
Summary:        Development files for miniz
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, CMake metadata, and the unversioned library
link for developing applications with miniz.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_EXAMPLES=ON \
  -DBUILD_FUZZERS=OFF \
  -DBUILD_HEADER_ONLY=OFF \
  -DBUILD_NO_STDIO=OFF \
  -DBUILD_TESTS=ON \
  -DINSTALL_PROJECT=ON
%cmake_build

%install
%cmake_install

%check
# Run the complete registered Catch2 suite first.
%ctest

# Upstream's six executable examples are additional API/integration checks.
pushd bin
for example in example1 example2 example3 example4 example5 example6; do
  case "$example" in
    example3)
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example c ../readme.md readme.md.z
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example d readme.md.z readme.md
      cmp ../readme.md readme.md
      ;;
    example4)
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example readme.md.z readme.md
      cmp ../readme.md readme.md
      ;;
    example5)
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example c ../readme.md readme.md.z
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example d readme.md.z readme.md
      cmp ../readme.md readme.md
      ;;
    *)
      LD_LIBRARY_PATH=../%{__cmake_builddir} ./$example
      ;;
  esac
done
popd

%files
%license LICENSE
%doc ChangeLog.md readme.md
%{_libdir}/libminiz.so.3*

%files devel
%license LICENSE
%{_includedir}/miniz/
%{_libdir}/cmake/miniz/
%{_libdir}/libminiz.so
%{_libdir}/pkgconfig/miniz.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.2-1
- Initial openEuler RISC-V package with Catch2 and all six example checks.
