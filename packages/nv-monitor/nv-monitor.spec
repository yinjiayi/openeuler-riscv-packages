# SPDX-License-Identifier: Apache-2.0
Name:           nv-monitor
Version:        1.12.0
Release:        3%{?dist}
Summary:        Local monitoring TUI, CSV logger, and Prometheus exporter for NVIDIA GPU systems
License:        MIT
URL:            https://github.com/wentbackward/nv-monitor
Source0:        nv-monitor-1.12.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
Local monitoring TUI, CSV logger, and Prometheus exporter for NVIDIA GPU systems

%prep
%autosetup -p1

%build
%make_build portable

%install
%{__install} -D -p -m 0755 nv-monitor %{buildroot}%{_bindir}/nv-monitor

%check
%make_build test

%files
%{_bindir}/nv-monitor
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.0-3
- Install the binary explicitly because the upstream target does not honor DESTDIR.

* Sun Aug 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.0-2
- Build the upstream portable target instead of using host-native ISA flags.
- Add the ncurses development files required by the monitor binary.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.0-1
- Initial openEuler RISC-V package from the full package inventory.
