# SPDX-License-Identifier: Apache-2.0
Name:           cmatrix
Version:        2.0
Release:        1%{?dist}
Summary:        Terminal Matrix-style display using ncurses
License:        GPL-3.0-only
URL:            https://github.com/abishekvashok/cmatrix
Source0:        cmatrix-2.0.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
CMatrix displays a scrolling, Matrix-style text animation in a terminal.

%prep
%autosetup -p1

%build
%cmake
%make_build

%install
DESTDIR=%{buildroot} %{__cmake} --install .
install -Dpm0644 cmatrix.1 %{buildroot}%{_mandir}/man1/cmatrix.1
rm -f %{buildroot}%{_datadir}/consolefonts/matrix.fnt
rm -f %{buildroot}%{_datadir}/consolefonts/matrix.psf.gz
rm -f %{buildroot}%{_libdir}/kbd/consolefonts/matrix.fnt
rm -f %{buildroot}%{_libdir}/kbd/consolefonts/matrix.psf.gz

%check
%{buildroot}%{_bindir}/cmatrix -h 2>&1 | grep -i 'usage'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README README.md
%{_bindir}/cmatrix
%{_mandir}/man1/cmatrix.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Initial openEuler RISC-V package.
