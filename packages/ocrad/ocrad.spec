# SPDX-License-Identifier: Apache-2.0
Name:           ocrad
Version:        0.29
Release:        1%{?dist}
Summary:        OCR (Optical Character Recognition) program based on a feature extraction method
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/ocrad/
Source0:        ocrad-0.29.tar.lz
BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  libpng-devel


%description
OCR (Optical Character Recognition) program based on a feature extraction method

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.29-1
- Initial openEuler RISC-V package from the full package inventory.
