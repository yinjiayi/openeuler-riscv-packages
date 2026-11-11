# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-hexdifferences
Version:        1.001
Release:        1%{?dist}
Summary:        Compare binary data as hexadecimal strings
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/release/STEFFENW/Test-HexDifferences-1.001
Source0:        Test-HexDifferences-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Cwd)
BuildRequires:  perl(English)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test::Builder::Module) >= 0.99
BuildRequires:  perl(Test::Differences) >= 0.60
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl(Text::Diff)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
Requires:       perl(Hash::Util)
Requires:       perl(Sub::Exporter)
Requires:       perl(Test::Builder::Module) >= 0.99
Requires:       perl(Text::Diff)

%description
Test::HexDifferences compares binary values and reports hexadecimal
differences using the bundled formatting module.

%prep
%autosetup -n Test-HexDifferences-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat > MODULE-BUILD-COMPAT-NOTICE <<'EOF'
The release's Makefile.PL uses the traditional template from
Module::Build::Compat 0.4218 (Ken Williams <kwilliams@cpan.org>).
https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-0.4218.tar.gz
SHA-256: 1ef0aa529a3f296f894a5e79240a77d71be60dd595e8cad3a0d04c7ea187c0d0

Copyright (c) 2001-2006 Ken Williams.  All rights reserved.

This library is free software; you can redistribute it and/or modify it
under the same terms as Perl itself.
EOF

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Test/HexDifferences.pm
test -f %{buildroot}%{perl_vendorlib}/Test/HexDifferences/HexDump.pm
test -f %{buildroot}%{_mandir}/man3/Test::HexDifferences.3pm
test -f %{buildroot}%{_mandir}/man3/Test::HexDifferences::HexDump.3pm

%check
make test TEST_VERBOSE=1

%files
%license Artistic-1.0-Perl.txt GPL-1.0.txt MODULE-BUILD-COMPAT-NOTICE
%doc README Changes
%{perl_vendorlib}/Test/HexDifferences.pm
%{perl_vendorlib}/Test/HexDifferences/
%{_mandir}/man3/Test::HexDifferences.3pm*
%{_mandir}/man3/Test::HexDifferences::HexDump.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.001-1
- Package the fixed CPAN release with original tests and template attribution.
