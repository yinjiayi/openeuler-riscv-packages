# SPDX-License-Identifier: Apache-2.0
Name:           libobject-accessor-perl
Version:        0.48
Release:        1%{?dist}
Summary:        Create Perl accessors with per-object storage
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND GPL-3.0-only
URL:            https://metacpan.org/dist/Object-Accessor
Source0:        Object-Accessor-0.48.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        GPL-3.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Params::Check) >= 0.34
BuildRequires:  perl(if)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(overload)
BuildRequires:  perl(constant)
BuildRequires:  perl(base)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Params::Check) >= 0.34
Requires:       perl(if)
Requires:       perl(deprecate)
Requires:       perl(strict)
Requires:       perl(vars)
Requires:       perl(overload)
Requires:       perl(constant)
Requires:       perl(base)
Requires:       perl(Tie::Scalar)

%description
Create Perl accessors with per-object storage

%prep
%autosetup -n Object-Accessor-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .
cat <<'DONOR_NOTICE' > EUMM-Upgrade-NOTICE
The WriteMakefile1 compatibility helper in Makefile.PL comes from
App-EUMM-Upgrade 0.21.
Copyright 2009 Alexandr Ciornii.
License: GPL-3.0-only; see the accompanying GPL-3.0.txt.
Source: https://cpan.metacpan.org/authors/id/C/CH/CHORNY/App-EUMM-Upgrade-0.21.tar.gz
This helper is build-only. It does not change the license of Object::Accessor.
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Object/Accessor.pm
test -f %{buildroot}%{_mandir}/man3/Object::Accessor.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt GPL-3.0.txt EUMM-Upgrade-NOTICE
%doc CHANGES
%{perl_vendorlib}/Object/Accessor.pm
%{_mandir}/man3/Object::Accessor.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.48-1
- Package the original module and tests with the build helper's separate notice.
