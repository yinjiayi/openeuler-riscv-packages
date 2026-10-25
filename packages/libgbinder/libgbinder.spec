# SPDX-License-Identifier: Apache-2.0
Name:           libgbinder
Version:        1.1.52
Release:        1%{?dist}
Summary:        GLib-style interface to binder
License:        BSD-3-Clause
URL:            https://github.com/mer-hybris/libgbinder
Source0:        libgbinder-1.1.52.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
GLib-style interface to binder

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
%license LICENSE
%doc README
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.52-1
- Initial openEuler RISC-V package from the full package inventory.
