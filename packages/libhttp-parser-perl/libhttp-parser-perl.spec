# SPDX-License-Identifier: Apache-2.0
Name:           perl-HTTP-Parser
Version:        0.06
Release:        1%{?dist}
Summary:        Incremental HTTP request and response parser for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTTP-Parser
Source0:        HTTP-Parser-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-HTTP-Message
BuildRequires:  perl-URI
BuildRequires:  perl-generators
Requires:       perl(HTTP::Request)
Requires:       perl(HTTP::Response)
Requires:       perl(URI)

%description
HTTP::Parser incrementally parses HTTP requests and responses into
HTTP::Request and HTTP::Response objects.

%prep
%autosetup -n HTTP-Parser-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the unchanged upstream default test: 22 assertions.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/HTTP/Parser.pm
%{_mandir}/man3/HTTP::Parser.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release with the unchanged default upstream test.
