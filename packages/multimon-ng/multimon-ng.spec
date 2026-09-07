# SPDX-License-Identifier: Apache-2.0
Name:           multimon-ng
Version:        1.6.0
Release:        1%{?dist}
Summary:        A fork of multimon that decodes multiple digital transmission modes
License:        GPL-2.0-or-later
URL:            https://github.com/EliasOenal/multimon-ng
Source0:        multimon-ng-1.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A fork of multimon that decodes multiple digital transmission modes

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
# RPM's brp-compress hook rewrites the installed manual page after the install phase.
# Keep it out of the pre-compression dynamic list and own either compressed or
# uncompressed output explicitly below.
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' \
  | grep -v '^%{_mandir}/man1/multimon-ng\.1$' \
  | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%{_mandir}/man1/multimon-ng.1*
%license COPYING
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
