# SPDX-License-Identifier: Apache-2.0
Name:           perl-Affix-Infix2Postfix
Version:        0.03
Release:        1%{?dist}
Summary:        Convert mathematical infix expressions to postfix notation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Affix-Infix2Postfix
Source0:        Affix-Infix2Postfix-%{version}.tar.gz
Source1:        Perl-Artistic
Source2:        Perl-Copying

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-podlators
BuildRequires:  perl-generators
Requires:       perl(Exporter)
Requires:       perl(AutoLoader)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Affix::Infix2Postfix translates infix expressions into postfix token lists
using a caller-supplied table of operators, functions and variable names.

%prep
%autosetup -n Affix-Infix2Postfix-%{version} -p1
# Preserve all six original source files, including the entire default test.
cat > .upstream.sha256 << 'EOF'
d4bba12fc5ad9f4b2892b307973e8c260fe776c7e2b9f6ae1d8108eaa32f513f  Makefile.PL
a6a5fb15f86ebd0c051298314c97aa99790907b129c24f6a6f370d1c25662c8a  Infix2Postfix.pm
c2820019e0d997b07927226c2bd1a4d6a0bbd44e733d98153e556333575834cc  Changes
020b41a9f6295eac23666342741e6604413eabc107f50331a81f8263ebe75589  test.pl
f2c2b1f929f8e924abae73ae71b817f5143a03d29c07aef7f883499b7ac6140e  README
37254fe0abc3a01e2538d09d36b443b771b62cb2d31cd917564aa8fb772dd4f5  MANIFEST
EOF
sha256sum -c .upstream.sha256
install -m 0644 %{SOURCE1} Artistic
install -m 0644 %{SOURCE2} Copying

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
# AutoSplit may emit autosplit.ix for the module's AutoLoader inheritance.
# Include only its package-specific tree if MakeMaker actually emits it.
: > .affix-auto.files
if test -d %{buildroot}%{perl_vendorlib}/auto/Affix/Infix2Postfix; then
    printf '%s\n' '%%dir %{perl_vendorlib}/auto/Affix' >> .affix-auto.files
    printf '%s\n' '%{perl_vendorlib}/auto/Affix/Infix2Postfix/' >> .affix-auto.files
fi

%check
sha256sum -c .upstream.sha256
# Unfiltered MakeMaker default test.pl: TAP load assertion and translation example.
%make_build test

%files -f .affix-auto.files
%license README Artistic Copying
%doc Changes
%dir %{perl_vendorlib}/Affix
%{perl_vendorlib}/Affix/Infix2Postfix.pm
%{_mandir}/man3/Affix::Infix2Postfix.3*

%changelog
* Fri Oct 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the fixed CPAN release without changing any original source or test.
- Include the original distribution grant and full pinned Perl license terms.
