# SPDX-License-Identifier: Apache-2.0
Name:           perl-Spiffy
Version:        0.46
Release:        1%{?dist}
Summary:        Spiffy Perl interface framework
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Spiffy
Source0:        Spiffy-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Filter
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-YAML
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(Filter::Util::Call)
Requires:       perl(Scalar::Util)
Requires:       perl(YAML)

%description
Spiffy is a Perl interface framework providing fields, mixins, exports and
source-filter helpers for object-oriented modules.

%prep
%autosetup -n Spiffy-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all default upstream tests, including its release-only POD skip.
%make_build test

%files
%license LICENSE
%doc Changes README CONTRIBUTING
%{perl_vendorlib}/Spiffy.pm
%{perl_vendorlib}/Spiffy.pod
%{perl_vendorlib}/Spiffy/mixin.pm
%{_mandir}/man3/Spiffy.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.46-1
- Package official CPAN release with all default upstream tests.
