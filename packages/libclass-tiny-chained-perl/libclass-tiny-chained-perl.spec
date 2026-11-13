# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-tiny-chained
Version:        0.004
Release:        1%{?dist}
Summary:        Chainable accessors for Class::Tiny
License:        Artistic-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:            https://metacpan.org/release/DBOOK/Class-Tiny-Chained-0.004
Source0:        Class-Tiny-Chained-0.004.tar.gz
Source1:        Dist-Zilla-6.007.LICENSE
Source2:        ReportPrereqs-0.025.LICENSE
Source3:        InstallGuide-1.200007.LICENSE
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  perl(Class::Tiny) >= 1.003
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Class::Tiny) >= 1.003

%description
Class::Tiny::Chained makes generated setter methods return the object so
that calls can be chained, while getter methods return attribute values.

%prep
%autosetup -n Class-Tiny-Chained-%{version} -p1
install -pm0644 %{SOURCE1} Dist-Zilla-6.007.LICENSE
install -pm0644 %{SOURCE2} ReportPrereqs-0.025.LICENSE
install -pm0644 %{SOURCE3} InstallGuide-1.200007.LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# The original generated prereq test loads a fixed in-tree .dd path;
# scope that compatibility lookup to the harness on modern Perl.
make test TEST_VERBOSE=1 TEST_SWITCHES=-I.

%files
%license LICENSE Dist-Zilla-6.007.LICENSE ReportPrereqs-0.025.LICENSE InstallGuide-1.200007.LICENSE
%doc README Changes CONTRIBUTING.md INSTALL
%{perl_vendorlib}/Class/Tiny/Chained.pm
%{_mandir}/man3/Class::Tiny::Chained.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.004-1
- Package the fixed CPAN release with original default tests and donor terms.
