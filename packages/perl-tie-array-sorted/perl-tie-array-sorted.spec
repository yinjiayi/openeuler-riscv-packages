# SPDX-License-Identifier: Apache-2.0
Name:           perl-Tie-Array-Sorted
Version:        1.41
Release:        1%{?dist}
Summary:        Perl tied arrays kept in sorted order
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Tie-Array-Sorted
Source0:        Tie-Array-Sorted-1.41.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators


%description
Tie::Array::Sorted provides tied arrays kept sorted after insertion, with a
custom comparator option. Tie::Array::Sorted::Lazy delays sorting until retrieval.

%prep
%autosetup -n Tie-Array-Sorted-%{version}
cp -p %{SOURCE1} gpl-2.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README gpl-2.0.txt
%doc Changes
%{perl_vendorlib}/Tie/Array/Sorted.pm
%{perl_vendorlib}/Tie/Array/Sorted/
%{_mandir}/man3/Tie::Array::Sorted.3*
%{_mandir}/man3/Tie::Array::Sorted::Lazy.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.41-1
- Package the fixed official release and all original default test files.
