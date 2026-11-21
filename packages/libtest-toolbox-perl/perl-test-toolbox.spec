# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-toolbox
Version:        0.4
Release:        1%{?dist}
Summary:        Test helpers for Perl comparisons and error checks
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Toolbox
Source0:        Test-Toolbox-0.4.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Cwd)
Requires:       perl(File::Basename)
Requires:       perl(Test::Builder::Module)
Requires:       perl(Exporter)
Requires:       perl(base)
Requires:       perl(strict)

%description
Test::Toolbox provides helpers for comparing Perl data structures and for
checking test files and exceptions.

%prep
%autosetup -n Test-Toolbox-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
# Do not enter upstream developer-only clear or host-global marker paths.
unset IDOCSDEV AUTOCLEAR
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Toolbox.pm
%{perl_vendorlib}/Test/Toolbox.pod
%{_mandir}/man3/Test::Toolbox.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Package Test::Toolbox with the original tests, POD, and complete license.
