# SPDX-License-Identifier: Apache-2.0
Name:           libregexp-optimizer-perl
Version:        0.23
Release:        1%{?dist}
Summary:        Optimize Perl regular-expression alternatives
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Regexp-Optimizer
Source0:        Regexp-Optimizer-%{version}.tar.gz
Source1:        Artistic-2.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Regexp::Assemble)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
Requires:       perl
Requires:       perl(Regexp::Assemble)

%description
Regexp::Optimizer rewrites Perl regular-expression alternatives into a
more compact pattern. Regexp::List is supplied for legacy compatibility.

%prep
%autosetup -n Regexp-Optimizer-%{version} -p1
cp -p %{SOURCE1} Artistic-2.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run all original default tests, including both POD checks.
make test TEST_VERBOSE=1

%files
%license Artistic-2.0.txt README
%doc Changes
%{perl_vendorlib}/Regexp/List.pm
%{perl_vendorlib}/Regexp/Optimizer.pm
%{_mandir}/man3/Regexp::List.3pm*
%{_mandir}/man3/Regexp::Optimizer.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23-1
- Package the official CPAN release with its original default tests.
