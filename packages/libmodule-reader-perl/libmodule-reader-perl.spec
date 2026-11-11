# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-reader
Version:        0.003003
Release:        2%{?dist}
Summary:        Read Perl module source using Perl include-path semantics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Module-Reader
Source0:        Module-Reader-0.003003.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Patch0:         0001-perl-538-object-hook-diagnostic.patch
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl >= 5.6.0
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(constant)
BuildRequires:  perl(mro)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Scalar::Util)
Requires:       perl(mro)
Requires:       perl(overload)

%description
Locate and read Perl module source using Perl-compatible include-path and
caller-supplied hook semantics.

%prep
%autosetup -n Module-Reader-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f -path '*/auto/Module/Reader/.packlist' -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Module/Reader.pm
%{_mandir}/man3/Module::Reader.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003003-2
- Match Perl 5.38's unsupported object-hook diagnostic without changing the upstream tests.

* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003003-1
- Package the fixed CPAN release with original tests and complete Perl terms.
