# SPDX-License-Identifier: Apache-2.0
Name:           perl-Convert-BinHex
Version:        1.125
Release:        1%{?dist}
Summary:        Perl encoder and decoder for Macintosh BinHex files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Convert-BinHex
Source0:        Convert-BinHex-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(Test::Most)

%description
Convert::BinHex encodes and decodes Macintosh BinHex streams. The package
also includes the upstream binhex.pl and debinhex.pl command-line tools.

%prep
%autosetup -n Convert-BinHex-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every default upstream test and its extended POD test. The release-only
# CPAN Changes check retains its upstream RELEASE_TESTING opt-in condition.
%make_build test
%make_build test TEST_FILES="xt/*.t"

%files
%license COPYING LICENSE
%doc Changes README README-TOO
%{_bindir}/binhex.pl
%{_bindir}/debinhex.pl
%{perl_vendorlib}/Convert/BinHex.pm
%{_mandir}/man1/binhex.pl.1*
%{_mandir}/man1/debinhex.pl.1*
%{_mandir}/man3/Convert::BinHex.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.125-1
- Package the official CPAN release, CLI tools, and upstream tests.
