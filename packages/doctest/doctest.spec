# SPDX-License-Identifier: Apache-2.0
Name:           doctest
Version:        2.5.2
Release:        1%{?dist}
Summary:        Lightweight feature-rich C++ testing framework
License:        MIT AND CC-BY-4.0 AND BSL-1.0 AND BSD-3-Clause
URL:            https://github.com/doctest/doctest
Source0:        doctest-2.5.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
doctest is a lightweight, feature-rich C++ testing framework.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DDOCTEST_WITH_TESTS=ON \
  -DDOCTEST_WITH_MAIN_IN_STATIC_LIB=ON
%cmake_build
%cmake_build --target doctest_with_main

%install
%cmake_install
install -Dpm 0644 %{_vpath_builddir}/libdoctest_with_main.a \
  %{buildroot}%{_libdir}/libdoctest_with_main.a

%check
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/doctest/
%{_libdir}/libdoctest_with_main.a
%{_libdir}/cmake/doctest/
%{_libdir}/pkgconfig/doctest.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-1
- Initial openEuler RISC-V package.
- Build the separately excluded static-library target before installation.
- Run the complete CTest suite serially under QEMU.
