# SPDX-License-Identifier: Apache-2.0
Name:           jpeginfo
Version:        1.7.1
Release:        1%{?dist}
Summary:        Inspect and validate JPEG image files
License:        GPL-3.0-or-later AND LicenseRef-Public-Domain
URL:            https://github.com/tjko/jpeginfo
Source0:        jpeginfo-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  make
BuildRequires:  python3

%description
jpeginfo prints dimensions and encoding details for JPEG files and can check
their structure for corruption. It also supports several digest and structured
output modes.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build test PYTHON=%{__python3}

%files
%license LICENSE COPYRIGHT
%doc README
%{_bindir}/jpeginfo
%{_mandir}/man1/jpeginfo.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.1-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
