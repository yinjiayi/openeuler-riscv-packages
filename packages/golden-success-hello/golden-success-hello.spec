# SPDX-License-Identifier: Apache-2.0
Name:           golden-success-hello
Version:        2.12.3
Release:        1%{?dist}
Summary:        GNU Hello golden package for successful RISC-V CI
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/hello/
Source0:        hello-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  texinfo

%description
GNU Hello prints a familiar greeting. This renamed package is pinned as the
successful end-to-end RPM and QEMU/RVA23 acceptance fixture.

%prep
%autosetup -n hello-%{version} -p1

%build
%configure --disable-nls
%make_build

%install
%make_install
# install-info owns this generated directory index; individual RPMs must not.
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/hello
%{_infodir}/hello.info*
%{_mandir}/man1/hello.1*

%changelog
* Sat Aug 08 2026 Package Automation <noreply@example.invalid> - 2.12.3-1
- Pin GNU Hello for the successful RISC-V golden path
