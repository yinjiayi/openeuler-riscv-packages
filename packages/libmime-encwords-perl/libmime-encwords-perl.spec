# SPDX-License-Identifier: Apache-2.0
Name:           perl-MIME-EncWords
Version:        1.015.0
Release:        1%{?dist}
Summary:        Encode and decode RFC 2047 MIME header words for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/MIME-EncWords
Source0:        MIME-EncWords-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Encode) >= 1.98
BuildRequires:  perl(MIME::Base64) >= 2.13
BuildRequires:  perl(MIME::Charset) >= 1.010.1
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Encode) >= 1.98
Requires:       perl(MIME::Base64) >= 2.13
Requires:       perl(MIME::Charset) >= 1.010.1

%description
MIME::EncWords handles RFC 2047 encoded words in message headers and includes
an alternative Encode::MIME::EncWords encoding interface.

%prep
%autosetup -n MIME-EncWords-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all six unmodified default t/*.t files, including optional POD checks.
%make_build test

%files
%license GPL ARTISTIC README
%doc Changes
%{perl_vendorlib}/MIME/EncWords.pm
%{perl_vendorlib}/MIME/EncWords/Defaults.pm.sample
%{perl_vendorlib}/Encode/MIME/EncWords.pm
%{perl_vendorlib}/POD2/JA/MIME/EncWords.pod
%{perl_vendorlib}/POD2/JA/Encode/MIME/EncWords.pod
%{_mandir}/man3/MIME::EncWords.3*
%{_mandir}/man3/Encode::MIME::EncWords.3*
%{_mandir}/man3/POD2::JA::MIME::EncWords.3*
%{_mandir}/man3/POD2::JA::Encode::MIME::EncWords.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.015.0-1
- Package the official CPAN release with all six default upstream tests.
