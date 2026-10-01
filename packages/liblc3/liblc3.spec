# SPDX-License-Identifier: Apache-2.0
Name:           liblc3
Version:        1.1.3
Release:        1%{?dist}
Summary:        Low Complexity Communication Codec library and tools
License:        Apache-2.0
URL:            https://github.com/google/liblc3
Source0:        liblc3-1.1.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Low Complexity Communication Codec library and tools

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
