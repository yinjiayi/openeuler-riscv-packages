# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-context
Version:        3.7
Release:        1%{?dist}
Summary:        Format highlighted context snippets for Perl
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Text-Context
Source0:        Text-Context-3.7.tar.gz
Source1:        GPL-2.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(constant)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Text::Context::EitherSide) >= 1.1
BuildRequires:  perl(UNIVERSAL::require) >= 0.03
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(constant)
Requires:       perl(HTML::Entities)
Requires:       perl(Text::Context::EitherSide) >= 1.1
Requires:       perl(UNIVERSAL::require) >= 0.03

%description
Format highlighted context snippets for Perl

%prep
%autosetup -n Text-Context-%{version}
cp -p %{SOURCE1} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license README GPL-2.0.txt
%doc Changes
%{perl_vendorlib}/Text/Context.pm
%{perl_vendorlib}/Text/Context/Para.pm
%{_mandir}/man3/Text::Context.3pm*
%{_mandir}/man3/Text::Context::Para.3pm*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.7-1
- Package the fixed upstream release with all original default tests.
