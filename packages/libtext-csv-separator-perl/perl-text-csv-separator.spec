# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-csv-separator
Version:        0.20
Release:        1%{?dist}
Summary:        Detect the field delimiter in a CSV file
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-CSV-Separator
Source0:        Text-CSV-Separator-0.20.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Text::CSV::Separator detects the likely field delimiter in a CSV file.

%prep
%autosetup -n Text-CSV-Separator-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/CSV/Separator.pm
%{_mandir}/man3/Text::CSV::Separator.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.20-1
- Package Text::CSV::Separator 0.20 and run its complete original default suite.
