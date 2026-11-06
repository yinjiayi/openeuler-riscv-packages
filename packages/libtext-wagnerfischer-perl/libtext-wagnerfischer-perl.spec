# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-WagnerFischer
Version:        0.04
Release:        1%{?dist}
Summary:        Calculate weighted Wagner-Fischer edit distances in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-WagnerFischer
Source0:        Text-WagnerFischer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Text::WagnerFischer calculates edit distances between strings. It also accepts
custom insertion, deletion and substitution costs and lists of candidates.

%prep
%autosetup -n Text-WagnerFischer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the original five-check test.pl. It prints failures but exits zero,
# so also require the same semantics with fatal assertions.
%make_build test
%{__perl} -Iblib/lib -MText::WagnerFischer=distance -e '
  die "unexpected version\n" unless $Text::WagnerFischer::VERSION eq "0.04";
  die "edit distance\n" unless distance("foo", "four") == 2;
  die "identity distance\n" unless distance("foo", "foo") == 0;
  die "weighted distance\n" unless distance([0,1,2], "foo", "four") == 3;
  my @words = ("four", "foo", "bar");
  my @distances = distance("foo", @words);
  die "candidate distances\n" unless join(",", @distances) eq "2,0,3";
  @distances = distance([0,5,3], "foo", @words);
  die "weighted candidates\n" unless join(",", @distances) eq "8,0,9";
'

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/WagnerFischer.pm
%{_mandir}/man3/Text::WagnerFischer.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package official CPAN release with original and fatal semantic tests.
