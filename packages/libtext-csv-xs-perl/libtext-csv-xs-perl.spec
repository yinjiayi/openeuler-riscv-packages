# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-CSV_XS
Version:        1.64
Release:        2%{?dist}
Summary:        Fast XS parser and writer for comma-separated values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-CSV_XS
Source0:        Text-CSV_XS-%{version}.tgz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Text-CSV >= 2.04
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl-generators

%description
Text::CSV_XS uses an XS extension to parse and compose comma-separated
values, including quoted fields and multiline records.

%prep
%autosetup -n Text-CSV_XS-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all 35 upstream default t/*.t files; no performance claim is made.
%make_build test
# Verify the target wrapper selects the just-built XS, rather than silently
# falling back to the PP backend as in Text::CSV::Encoded PR #2296.
PERL5LIB="$PWD/blib/lib:$PWD/blib/arch" PERL_TEXT_CSV=1 %{__perl} -MText::CSV -e '
  die "unexpected wrapper version\n" unless $Text::CSV::VERSION eq "2.04";
  die "unexpected XS version\n" unless $Text::CSV_XS::VERSION eq "1.64";
  my $csv = Text::CSV->new({binary => 1})
    or die "wrapper initialization failed\n";
  die "wrapper did not select XS\n" unless $csv->is_xs;
  $csv->parse(q{"a,b",c}) or die "wrapper parse failed\n";
  my @fields = $csv->fields;
  die "wrapper parse mismatch\n"
    unless @fields == 2 && $fields[0] eq "a,b" && $fields[1] eq "c";
  print "Text::CSV 2.04 selects Text::CSV_XS 1.64\n";
'

%files
%doc README ChangeLog CONTRIBUTING.md SECURITY.md LOVE_LETTER.md examples
%{perl_vendorarch}/Text/CSV_XS.pm
%{perl_vendorarch}/auto/Text/CSV_XS/
%{_mandir}/man3/Text::CSV_XS.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.64-2
- Verify target Text::CSV wrapper selects the newly built XS backend.
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.64-1
- Package official newer CPAN XS release and complete default suite.
