# SPDX-License-Identifier: Apache-2.0
Name:           wmime
Version:        1.1.0
Release:        1%{?dist}
Summary:        Library for working with RFC 5322, MIME messages and IMAP/POP/SMTP
License:        GPL-3.0-or-later
URL:            https://github.com/grommunio/wmime
Source0:        wmime-1.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Library for working with RFC 5322, MIME messages and IMAP/POP/SMTP

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING
%license COPYING.OpenSSL
%doc README
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
