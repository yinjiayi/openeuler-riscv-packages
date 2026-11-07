# SPDX-License-Identifier: Apache-2.0
Name:           libperl-version-perl
Version:        1.019
Release:        1%{?dist}
Summary:        Parse and manipulate Perl version numbers
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Perl-Version
Source0:        Perl-Version-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Getopt::Long) >= 2.34
BuildRequires:  perl(Pod::Usage) >= 1.3
BuildRequires:  perl(Scalar::Util)
Requires:       perl
Requires:       perl(Getopt::Long) >= 2.34
Requires:       perl(Pod::Usage) >= 1.3

%description
Parse, compare and manipulate Perl version numbers. The perl-reversion
utility can inspect and update version strings in a Perl source tree.

%prep
%setup -q -n Perl-Version-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 \
    INSTALLVENDORBIN=%{_bindir} INSTALLVENDORSCRIPT=%{_bindir} \
    INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE
%doc README.pod Changes Notes.txt SECURITY.md
%{perl_vendorlib}/Perl/Version.pm
%{_bindir}/perl-reversion
%{_mandir}/man1/perl-reversion.1*
%{_mandir}/man3/Perl::Version.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.019-1
- Package the pinned upstream release, module, utility, and original tests.
