# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-refresh
Version:        0.18
Release:        1%{?dist}
Summary:        Reload modified Perl modules
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Module-Refresh
Source0:        Module-Refresh-0.18.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.36
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Path::Class)
Requires:       perl
Requires:       perl(File::Temp) >= 0.19
Requires:       perl(strict)
Requires:       perl(vars)

%description
Reload modified Perl modules

%prep
%autosetup -n Module-Refresh-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Module/Refresh.pm
%{_mandir}/man3/Module::Refresh.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18-1
- Package the verified CPAN release and retain all four upstream tests.
