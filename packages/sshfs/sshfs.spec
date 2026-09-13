# SPDX-License-Identifier: Apache-2.0
Name:           sshfs
Version:        3.7.6
Release:        1%{?dist}
Summary:        FUSE client based on the SSH File Transfer Protocol
License:        GPL-2.0-or-later
URL:            https://github.com/libfuse/sshfs
Source0:        sshfs-3.7.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
FUSE client based on the SSH File Transfer Protocol

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.7.6-1
- Initial openEuler RISC-V package from the full package inventory.
