# SPDX-License-Identifier: Apache-2.0
Name:           stow
Version:        2.4.1
Release:        1%{?dist}
Summary:        Manage installation trees with symbolic links
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/stow/
Source0:        stow-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl-Test-Output
BuildRequires:  perl-Test-Simple

%description
GNU Stow manages separate software or data trees by exposing them through a
common target directory using symbolic links. It includes the stow and
chkstow commands plus the reusable Stow Perl modules.

%prep
%autosetup -p1

%build
export STRICT_TESTS=1
%configure --with-pmdir=%{perl_vendorlib}
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%{__make} V=1 check

%files
%license COPYING
%{_bindir}/chkstow
%{_bindir}/stow
%{perl_vendorlib}/Stow.pm
%{perl_vendorlib}/Stow/
%{_infodir}/stow.info*
%{_mandir}/man8/stow.8*
%{_docdir}/stow/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package with all 478 upstream assertions.
