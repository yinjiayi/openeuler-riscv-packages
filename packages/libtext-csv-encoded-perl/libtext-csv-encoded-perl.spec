# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-CSV-Encoded
Version:        0.25
Release:        1%{?dist}
Summary:        Encoding-aware CSV processing in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-CSV-Encoded
Source0:        Text-CSV-Encoded-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Text::CSV) >= 1.31
BuildRequires:  perl(Text::CSV_PP)
BuildRequires:  perl(Text::CSV_XS)
BuildRequires:  perl-generators
Requires:       perl(Text::CSV) >= 1.31
Requires:       perl(Text::CSV_XS)

%description
Text::CSV::Encoded adds input and output character-encoding handling to
Text::CSV. Both the pure-Perl and XS CSV backends are supported.

%prep
%autosetup -n Text-CSV-Encoded-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 14 default t/*.t files, including PP, XS and POD checks.
%make_build test

%files
%license LICENSE
%doc Changes README.pod
%{perl_vendorlib}/Text/CSV/Encoded.pm
%{perl_vendorlib}/Text/CSV/Encoded/
%{_mandir}/man3/Text::CSV::Encoded*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.25-1
- Package official CPAN release with complete PP, XS and POD tests.
