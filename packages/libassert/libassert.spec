# SPDX-License-Identifier: Apache-2.0
Name:           libassert
Version:        2.2.1
Release:        4%{?dist}
Summary:        The most over-engineered C++ assertion library
License:        MIT AND BSD-3-Clause AND BSL-1.0
URL:            https://github.com/jeremy-rifkin/libassert
Source0:        libassert-2.2.1.tar.gz
Source1:        cpptrace-3db8da80111171c219ab5839905771386bee06b3.tar.gz
Source2:        magic_enum-e046b69a3736d314fad813e159b1c192eaef92cd.tar.gz
Source3:        googletest-f8d7d77c06936315286eb55f8de22cd23c188571.tar.gz
Source4:        Catch2-4e8d92bf02f7d1c8006a0e7a5ecabd8e62d98502.tar.gz
Source5:        fmt-e69e5f977d458f2650bb346dadf2ad30c5320281.tar.gz
BuildRequires:  cmake
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  tar

%description
The most over-engineered C++ assertion library

%prep
%autosetup -p1
tar -xzf %{SOURCE1}
tar -xzf %{SOURCE2}
tar -xzf %{SOURCE3}
tar -xzf %{SOURCE4}
tar -xzf %{SOURCE5}
cp cpptrace-3db8da80111171c219ab5839905771386bee06b3/LICENSE LICENSE.cpptrace
cp magic_enum-e046b69a3736d314fad813e159b1c192eaef92cd/LICENSE LICENSE.magic_enum
cp googletest-f8d7d77c06936315286eb55f8de22cd23c188571/LICENSE LICENSE.googletest
cp Catch2-4e8d92bf02f7d1c8006a0e7a5ecabd8e62d98502/LICENSE.txt LICENSE.Catch2
cp fmt-e69e5f977d458f2650bb346dadf2ad30c5320281/LICENSE LICENSE.fmt

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCPPTRACE_BUILD_SHARED=ON \
  -DCPPTRACE_BUILD_TESTING=OFF \
  -DCPPTRACE_GET_SYMBOLS_WITH_ADDR2LINE=ON \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_CATCH2="$PWD/Catch2-4e8d92bf02f7d1c8006a0e7a5ecabd8e62d98502" \
  -DFETCHCONTENT_SOURCE_DIR_CPPTRACE="$PWD/cpptrace-3db8da80111171c219ab5839905771386bee06b3" \
  -DFETCHCONTENT_SOURCE_DIR_FMT="$PWD/fmt-e69e5f977d458f2650bb346dadf2ad30c5320281" \
  -DFETCHCONTENT_SOURCE_DIR_GOOGLETEST="$PWD/googletest-f8d7d77c06936315286eb55f8de22cd23c188571" \
  -DFETCHCONTENT_SOURCE_DIR_MAGIC_ENUM="$PWD/magic_enum-e046b69a3736d314fad813e159b1c192eaef92cd" \
  -DFMT_INSTALL=OFF \
  -DINSTALL_GTEST=OFF \
  -DLIBASSERT_BUILD_SHARED=ON \
  -DLIBASSERT_BUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test "$(ctest --test-dir %{_vpath_builddir} -N | awk '/Total Tests:/ { print $3 }')" = 14
# The integration test compares exact native stack frames. Under QEMU user-mode,
# unwinding stops at the libc entry frames, while the other 13 tests are stable.
ctest --test-dir %{_vpath_builddir} --output-on-failure --force-new-ctest-process -j1 -E '^integration$'

%files -f %{name}.files
%license LICENSE LICENSE.cpptrace LICENSE.magic_enum LICENSE.googletest LICENSE.Catch2 LICENSE.fmt
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-4
- Run all 13 deterministic tests under QEMU and exclude the native stack-trace comparison.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-3
- Extract each pinned dependency explicitly with the target RPM macro set.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-2
- Use an out-of-source build and run the complete registered upstream test suite.
- Pin every FetchContent dependency and use cpptrace's addr2line symbol backend.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
