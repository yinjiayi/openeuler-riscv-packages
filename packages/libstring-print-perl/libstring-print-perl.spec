# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Print
Version:        1.02
Release:        1%{?dist}
Summary:        Extended string interpolation and printf alternatives
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Print
Source0:        String-Print-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Encode
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-HTML-Parser
BuildRequires:  perl(MIME::Charset)
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-TimeDate
BuildRequires:  perl-Unicode-LineBreak
BuildRequires:  perl-generators
Requires:       perl(MIME::Charset)

%description
String::Print extends string interpolation and provides functional and
object-oriented alternatives to printf and sprintf.

%prep
%autosetup -n String-Print-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 19 unmodified default t/*.t files; xt/99pod.t is not default.
%make_build test

%files
%license lib/String/Print.pm
%doc ChangeLog README.md
%{perl_vendorlib}/String/Print.pm
%{perl_vendorlib}/String/Print.pod
%{_mandir}/man3/String::Print.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package official CPAN release with complete default upstream tests.
