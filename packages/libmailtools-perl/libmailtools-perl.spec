# SPDX-License-Identifier: Apache-2.0
Name:           perl-MailTools
Version:        2.22
Release:        1%{?dist}
Summary:        Perl modules for handling basic Internet mail
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/MailTools
Source0:        MailTools-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Date::Format)
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(Net::Domain)
BuildRequires:  perl(Net::NNTP)
BuildRequires:  perl(Net::SMTP)
Requires:       perl(Date::Format)
Requires:       perl(Date::Parse)
Requires:       perl(Net::Domain)
Requires:       perl(Net::NNTP)
Requires:       perl(Net::SMTP)

%description
MailTools provides Perl modules for parsing, composing, and sending basic
Internet mail, including Mail::Mailer required by ytnefprocess.

%prep
%autosetup -n MailTools-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every test in upstream's standard t/ and extended POD suites.
%make_build test
%make_build test TEST_FILES="xt/*.t"

%files
%doc ChangeLog README README.md README.demos
%{perl_vendorlib}/Mail/
%{perl_vendorlib}/MailTools.pm
%{perl_vendorlib}/MailTools.pod
%{_mandir}/man3/Mail*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.22-1
- Package the official CPAN release and complete standard test suite.
