# SPDX-License-Identifier: Apache-2.0
Name:           vera
Version:        1.24
Release:        1%{?dist}
Summary:        GNU Virtual Entity of Relevant Acronyms data set
License:        GFDL-1.3-or-later
URL:            https://www.gnu.org/software/vera/
Source0:        vera-1.24.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  texinfo
BuildArch:      noarch


%description
GNU Virtual Entity of Relevant Acronyms data set

%prep
%autosetup -p1

%build
makeinfo --no-split -o vera.info vera.texi

%install
install -d %{buildroot}%{_datadir}/vera %{buildroot}%{_infodir}
install -m 0644 vera.[0a-z] %{buildroot}%{_datadir}/vera/
install -m 0644 vera.info %{buildroot}%{_infodir}/

%check
test -s vera.info
test -s vera.a

%files
%license fdl-1.3.texi
%doc README
%{_datadir}/vera/
%{_infodir}/vera.info*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.24-1
- Initial openEuler RISC-V package from the full package inventory.
