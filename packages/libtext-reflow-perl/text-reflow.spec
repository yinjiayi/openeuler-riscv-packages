# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-reflow
Version:        1.17
Release:        1%{?dist}
Summary:        Reflow paragraphs using Knuth's line-breaking algorithm
License:        GPL-3.0-or-later AND GPL-2.0-or-later
URL:            https://metacpan.org/dist/Text-Reflow
Source0:        Text-Reflow-1.17.tar.gz
Source1:        GPL-2.0.txt
Source2:        GPL-3.0.txt
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(integer)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Simple)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(DynaLoader)
Requires:       perl(Exporter)
Requires:       perl(integer)
Requires:       perl(strict)
Requires:       perl(vars)
Requires:       perl(warnings)

%description
Text::Reflow reflows paragraphs using Knuth's line-breaking algorithm.
This package includes the Perl XS module and the reflow command.

%prep
%autosetup -n Text-Reflow-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

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
%license GPL-2.0.txt GPL-3.0.txt
%doc README Changes
%{_bindir}/reflow
%{perl_vendorarch}/Text/Reflow.pm
%{perl_vendorarch}/auto/Text/Reflow/
%{_mandir}/man1/reflow.1*
%{_mandir}/man3/Text::Reflow.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.17-1
- Package the verified CPAN release with its unmodified upstream tests.
