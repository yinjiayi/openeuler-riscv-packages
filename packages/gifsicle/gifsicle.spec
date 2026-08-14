# SPDX-License-Identifier: Apache-2.0

Name:           gifsicle
Version:        1.96
Release:        1%{?dist}
Summary:        Command-line tools for manipulating GIF images
License:        GPL-2.0-only
URL:            https://www.lcdf.org/gifsicle/
Source0:        gifsicle-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  libX11-devel
BuildRequires:  make
BuildRequires:  perl

%description
Gifsicle creates, edits, optimizes, and inspects GIF images and animations.
It also includes gifdiff for visual comparison and gifview for displaying GIF
animations on an X11 display.

%prep
%autosetup -p1

%build
%configure --enable-gifview
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc NEWS.md README.md
%{_bindir}/gifdiff
%{_bindir}/gifsicle
%{_bindir}/gifview
%{_mandir}/man1/gifdiff.1*
%{_mandir}/man1/gifsicle.1*
%{_mandir}/man1/gifview.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.96-1
- Initial openEuler RISC-V package with all programs and upstream tests.
