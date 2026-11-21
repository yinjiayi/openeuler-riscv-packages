# SPDX-License-Identifier: Apache-2.0
Name:           libscalar-util-numeric-perl
Version:        0.40
Release:        1%{?dist}
Summary:        Classify numeric values in Perl scalars
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Scalar-Util-Numeric
Source0:        Scalar-Util-Numeric-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::Complex)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(overload)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl

%description
Scalar::Util::Numeric exposes Perl's numeric classification for integer,
decimal, nonnumeric, and special scalar values through its upstream XS code.

%prep
%setup -q -n Scalar-Util-Numeric-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build
test -s blib/arch/auto/Scalar/Util/Numeric/Numeric.so

%install
make pure_install DESTDIR=%{buildroot}

%check
make test
# The original POD test looks outside this build directory. Preserve it,
# then independently validate the actual staged module's documentation.
test -s blib/lib/Scalar/Util/Numeric.pm
%{__perl} -MTest::Pod -e 'Test::Pod::all_pod_files_ok("blib")'

%files
%license README ppport.h
%doc Changes
%{perl_vendorarch}/Scalar/Util/Numeric.pm
%{perl_vendorarch}/auto/Scalar/Util/Numeric/
%{_mandir}/man3/Scalar::Util::Numeric.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.40-1
- Package the fixed XS release, preserve its default suite, and check the real POD.
