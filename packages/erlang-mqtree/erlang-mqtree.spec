# SPDX-License-Identifier: Apache-2.0
Name:           erlang-mqtree
Version:        1.0.19
Release:        1%{?dist}
Summary:        Index tree for MQTT topic filters
License:        Apache-2.0
URL:            https://github.com/processone/mqtree
Source0:        erlang-mqtree-1.0.19.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Index tree for MQTT topic filters

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.19-1
- Initial openEuler RISC-V package from the full package inventory.
