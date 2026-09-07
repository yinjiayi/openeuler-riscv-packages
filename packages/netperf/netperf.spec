# SPDX-License-Identifier: Apache-2.0
Name:           netperf
Version:        2.7.0
Release:        6%{?dist}
Summary:        Benchmarking tool for many different types of networking
License:        MIT
URL:            https://github.com/HewlettPackard/netperf
Source0:        netperf-2.7.0.tar.gz
Patch0:         patches/0001-linux-declare-sendfile-and-sched-affinity.patch
Patch1:         patches/0002-net-uuid-include-unistd.patch
BuildRequires:  gcc
BuildRequires:  make

%description
Benchmarking tool for many different types of networking

%prep
%autosetup -p1 -n netperf-netperf-2.7.0

%build
%configure CPPFLAGS="-D_GNU_SOURCE" CFLAGS="%{optflags} -fcommon"
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-6
- Retain GCC common-symbol semantics required by the 2.7.0 sources.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-5
- Backport the upstream unistd declarations for the UUID helper.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-4
- Enable GNU declarations consistently for all Linux source files.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-3
- Declare the Linux sendfile and CPU affinity interfaces for GCC 14.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-2
- Use the verified GitHub tag archive's actual top-level source directory.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
