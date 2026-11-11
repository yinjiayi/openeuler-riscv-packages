# SPDX-License-Identifier: Apache-2.0
Name:           perl-term-encoding
Version:        0.03
Release:        1%{?dist}
Summary:        Detect the character encoding expected by a terminal
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MIYAGAWA/Term-Encoding-0.03
Source0:        Term-Encoding-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(I18N::Langinfo)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(I18N::Langinfo)

%description
Term::Encoding determines the current terminal encoding using platform
locale information, with environment-variable fallback.

%prep
%autosetup -n Term-Encoding-%{version} -p1
cat > DIST-ZILLA-GENERATED-NOTICE <<'NOTICE'
Makefile.PL and the generated portion of t/author-pod-syntax.t derive
from Dist::Zilla 6.012's MakeMaker and PodSyntaxTests templates.
Copyright (c) 2018 by Ricardo SIGNES.
These templates are available under the same terms as Perl 5 itself.
The complete applicable GPL and Artistic license terms are in LICENSE.
Origin: https://metacpan.org/release/RJBS/Dist-Zilla-6.012
NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Term/Encoding.pm
test -f %{buildroot}%{_mandir}/man3/Term::Encoding.3pm

%check
make test TEST_VERBOSE=1

%files
%license LICENSE DIST-ZILLA-GENERATED-NOTICE
%doc README Changes
%{perl_vendorlib}/Term/Encoding.pm
%{_mandir}/man3/Term::Encoding.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the fixed CPAN release and preserve its original default tests.
