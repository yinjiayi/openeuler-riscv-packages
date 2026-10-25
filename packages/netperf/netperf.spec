# SPDX-License-Identifier: Apache-2.0
Name:           netperf
Version:        2.7.0
Release:        8%{?dist}
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
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog
%{_bindir}/netperf
%{_bindir}/netserver
%{_infodir}/netperf.info*
%{_mandir}/man1/netperf.1*
%{_mandir}/man1/netserver.1*

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-8
- Remove the generated shared info directory index from the package buildroot.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-7
- List compressed manual and info files with RPM path macros.

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
