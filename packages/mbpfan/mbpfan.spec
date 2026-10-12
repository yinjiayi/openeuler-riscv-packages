# SPDX-License-Identifier: Apache-2.0
Name:           mbpfan
Version:        2.4.0
Release:        1%{?dist}
Summary:        A simple daemon to control fan speed on all MacBook/MacBook Pros
License:        GPL-3.0-or-later
URL:            https://github.com/linux-on-mac/mbpfan
Source0:        mbpfan-2.4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A simple daemon to control fan speed on all MacBook/MacBook Pros

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
