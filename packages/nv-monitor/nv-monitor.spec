# SPDX-License-Identifier: Apache-2.0
Name:           nv-monitor
Version:        1.12.0
Release:        1%{?dist}
Summary:        Local monitoring TUI, CSV logger, and Prometheus exporter for NVIDIA GPU systems
License:        MIT
URL:            https://github.com/wentbackward/nv-monitor
Source0:        nv-monitor-1.12.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Local monitoring TUI, CSV logger, and Prometheus exporter for NVIDIA GPU systems

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.0-1
- Initial openEuler RISC-V package from the full package inventory.
