# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Report
Version:        1.001
Release:        1%{?dist}
Summary:        Flexible text, HTML and CSV report generation in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Report
Source0:        Data-Report-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::CSV) >= 1
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.46
BuildRequires:  perl-generators
Requires:       perl(ExtUtils::MakeMaker) >= 6.46
Requires:       perl(Test::More)
Requires:       perl(Text::CSV) >= 1

%description
Data::Report creates flexible text, HTML and CSV reports using a common
layout and plugin interface.

%prep
%autosetup -n Data-Report-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all 23 default upstream test files without exclusions or changes.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/Report.pm
%{perl_vendorlib}/Data/Report/Base.pm
%{perl_vendorlib}/Data/Report/Plugin/*.pm
%{_mandir}/man3/Data::Report.3*
%{_mandir}/man3/Data::Report::Base.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.001-1
- Package the official CPAN release with its unchanged default test suite.
