# SPDX-License-Identifier: MIT
Name:           liblcf
Version:        0.8.1
Release:        1%{?dist}
Summary:        Library for RPG Maker 2000 and 2003 game data
License:        MIT AND BSD-3-Clause AND BSL-1.0
URL:            https://easyrpg.org/
Source0:        https://codeload.github.com/EasyRPG/liblcf/tar.gz/92c4450a1bc1acb58bd02bbb99b57e5036919cdf#/liblcf-0.8.1.tar.gz
Source1:        https://raw.githubusercontent.com/boostorg/boost/ab7968a0bbcf574a7859240d1d8443f58ed6f6cf/LICENSE_1_0.txt#/BSL-1.0.txt
Source2:        https://raw.githubusercontent.com/doctest/doctest/ae7a13539fb71f270b87eb2e874fbac80bc8dda2/LICENSE.txt#/doctest-MIT.txt
Patch0:         patches/0001-defer-staged-mime-cache.patch
Patch1:         patches/0002-add-installed-checks.patch
Patch2:         patches/0003-find-inih-pkgconfig-module.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  inih-devel
BuildRequires:  libicu-devel
BuildRequires:  expat-devel
BuildRequires:  shared-mime-info
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  grep
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  gawk
Requires:       /sbin/ldconfig
Requires(posttrans): shared-mime-info
Requires(postun): shared-mime-info

%description
Read and write RPG Maker 2000/2003 LCF data. The upstream default shared library,
INI parsing, ICU encodings, XML support, tools and MIME integration are retained.

%package devel
Summary:        Development interfaces and installed checks for liblcf
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-tools = %{version}-%{release}
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       pkgconf
Requires:       inih-devel
Requires:       libicu-devel
Requires:       expat-devel
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       grep

%description devel
Original public headers, linker symlink, pkg-config and CMake exports. Includes
all ten original unit-test translation units and their bundled doctest header,
plus separate downstream checks against the installed interfaces.

%package tools
Summary:        LCF string extraction and XML conversion tools
Requires:       %{name} = %{version}-%{release}

%description tools
The original lcfstrings and lcf2xml programs, built with their default features.

%prep
%setup -q -n liblcf-92c4450a1bc1acb58bd02bbb99b57e5036919cdf
%patch0 -p1
%patch1 -p1
%patch2 -p1
cp %{SOURCE1} BSL-1.0.txt
cp %{SOURCE2} doctest-MIT.txt

%build
# No feature/test/tool switches: retain every upstream default.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_LIBRARY_PATH:PATH=%{_libdir} -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -UNDEBUG" -DCMAKE_SHARED_LINKER_FLAGS="%{build_ldflags}" -DCMAKE_EXE_LINKER_FLAGS="%{build_ldflags}"
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/liblcf/tests
install -m 0644 tests/*.cpp tests/doctest.h %{buildroot}%{_datadir}/liblcf/tests/
install -m 0644 downstream/consumer.cpp downstream/CMakeLists.txt downstream/LICENSE.MIT %{buildroot}%{_datadir}/liblcf/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/liblcf/run-tests.sh
(
    cd %{buildroot}%{_datadir}/liblcf
    find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)

%check
# Original custom check target, not CTest; no filtering or source modifications.
cmake --build build --target check --parallel %{?_smp_build_ncpus}
bash %{buildroot}%{_datadir}/liblcf/run-tests.sh %{buildroot}

%post -p /sbin/ldconfig

%posttrans
update-mime-database %{_datadir}/mime

%postun
/sbin/ldconfig
if [ "$1" -eq 0 ]; then
    update-mime-database %{_datadir}/mime
fi

%files
%license COPYING BSL-1.0.txt doctest-MIT.txt src/lcf/inireader.h src/lcf/third_party/span.h tests/doctest.h
%doc README.md AUTHORS.md
%{_libdir}/liblcf.so.0
%{_datadir}/mime/packages/liblcf.xml

%files devel
%license downstream/LICENSE.MIT
%{_includedir}/lcf/
%{_libdir}/liblcf.so
%{_libdir}/pkgconfig/liblcf.pc
%{_libdir}/cmake/liblcf/
%{_datadir}/liblcf/

%files tools
%{_bindir}/lcfstrings
%{_bindir}/lcf2xml

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.8.1-1
- Package fixed official release with all default features and original tests.
