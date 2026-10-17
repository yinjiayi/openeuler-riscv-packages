# SPDX-License-Identifier: Apache-2.0
Name:           sexpect
Version:        2.3.15
Release:        4%{?dist}
Summary:        Expect for shells
License:        GPL-3.0-or-later
URL:            https://github.com/clarkwang/sexpect
Source0:        sexpect-2.3.15.tar.gz
Patch0:         patches/0001-cmake-shorten-test-socket-paths.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  procps-ng

%description
Expect for shells

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) ! -path '%{buildroot}%{_mandir}/*' -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md
%{_mandir}/man1/sexpect.1*

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.15-4
- Keep the compressed manual page out of the pre-compression file manifest.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.15-3
- Keep generated test sockets within the Linux sockaddr_un path limit.
- Add procps-ng for the upstream process-state test.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.15-2
- Configure the source and out-of-source build directories explicitly.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.15-1
- Initial openEuler RISC-V package from the full package inventory.
