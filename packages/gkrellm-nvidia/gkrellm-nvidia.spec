# SPDX-License-Identifier: Apache-2.0
Name:           gkrellm-nvidia
Version:        1.3.2
Release:        1%{?dist}
Summary:        A plugin for gkrellm2 which displays nVidia GPU status
License:        GPL-2.0-or-later
URL:            https://github.com/carcass82/gkrellm-nvidia
Source0:        gkrellm-nvidia-1.3.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A plugin for gkrellm2 which displays nVidia GPU status

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
