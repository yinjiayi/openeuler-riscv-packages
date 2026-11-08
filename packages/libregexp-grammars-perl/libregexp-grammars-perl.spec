# SPDX-License-Identifier: Apache-2.0
Name:           libregexp-grammars-perl
Version:        1.058
Release:        1%{?dist}
Summary:        Parse recursive grammars with Perl regular expressions
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND GPL-2.0-or-later
URL:            https://metacpan.org/dist/Regexp-Grammars
Source0:        Regexp-Grammars-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        miscfiles-1.4.2.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(version)
Requires:       perl
Requires:       perl(Test::More)
Requires:       perl(version)

%description
Regexp::Grammars adds grammar rules and structured captures to Perl
regular expressions, allowing recursive descent parsing.

%prep
%autosetup -n Regexp-Grammars-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt
# Preserve the notices for the source-only demo dictionary; never execute it.
tar -xOf %{SOURCE3} miscfiles-1.4.2/README > GNU-miscfiles-README.txt
tar -xOf %{SOURCE3} miscfiles-1.4.2/dict-README > GNU-web2-README.txt
tar -xOf %{SOURCE3} miscfiles-1.4.2/COPYING > GNU-GPL-2.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Keep all original test files, including POD.
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%license GNU-miscfiles-README.txt GNU-web2-README.txt GNU-GPL-2.0.txt
%doc Changes
%{perl_vendorlib}/Regexp/Grammars.pm
%{_mandir}/man3/Regexp::Grammars.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.058-1
- Package the official CPAN release with original tests and source notices.
