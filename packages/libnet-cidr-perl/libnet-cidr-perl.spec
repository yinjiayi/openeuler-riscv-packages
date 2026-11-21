# SPDX-License-Identifier: Apache-2.0
Name:           libnet-cidr-perl
Version:        0.27
Release:        1%{?dist}
Summary:        Manipulate IPv4 and IPv6 CIDR network blocks in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-CIDR
Source0:        Net-CIDR-0.27.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.10.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)

%description
Manipulate IPv4 and IPv6 CIDR network blocks in Perl

%prep
%autosetup -n Net-CIDR-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
# Keep the upstream RPM recipe and generator as source data only.
%{__perl} - INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 <<'MAKEMAKER'
use strict;
use warnings;
use ExtUtils::MakeMaker ();
my $original = \&ExtUtils::MakeMaker::WriteMakefile;
{
    no warnings 'redefine';
    local *ExtUtils::MakeMaker::WriteMakefile = sub {
        my %%args = @_;
        my $generators = $args{PL_FILES};
        die "unexpected generated files" unless ref($generators) eq 'HASH'
            && keys(%%$generators) == 1 && ($generators->{'Net-CIDR.spec.PL'} // '') eq 'Net-CIDR.spec';
        $args{PL_FILES} = {};
        return $original->(%%args);
    };
    my $result = do './Makefile.PL';
    die "Makefile.PL: $@ $!" unless defined $result;
}
MAKEMAKER
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Net/CIDR.pm
test -f %{buildroot}%{_mandir}/man3/Net::CIDR.3pm

%check
make test TEST_VERBOSE=1

%files
%license COPYING Artistic-1.0-Perl.txt GPL-1.0.txt
%doc README ChangeLog
%{perl_vendorlib}/Net/CIDR.pm
%{_mandir}/man3/Net::CIDR.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27-1
- Package the original module and tests without invoking the archived RPM recipe.
