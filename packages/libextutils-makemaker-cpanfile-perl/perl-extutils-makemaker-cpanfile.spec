# SPDX-License-Identifier: Apache-2.0
Name:           perl-extutils-makemaker-cpanfile
Version:        0.11
Release:        1%{?dist}
Summary:        Use cpanfile to list dependencies for Perl distributions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/ExtUtils-MakeMaker-CPANfile
Source0:        ExtUtils-MakeMaker-CPANfile-0.11.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.141170
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::CPANfile)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(strict)
BuildRequires:  perl(version) >= 0.76
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(CPAN::Meta::Converter) >= 2.141170
Requires:       perl(CPAN::Meta::Requirements)
Requires:       perl(Cwd)
Requires:       perl(ExtUtils::MakeMaker) >= 6.17
Requires:       perl(File::Path)
Requires:       perl(File::Spec::Functions)
Requires:       perl(Module::CPANfile)
Requires:       perl(Test::More) >= 0.88
Requires:       perl(strict)
Requires:       perl(version) >= 0.76
Requires:       perl(warnings)

%description
Use cpanfile to list dependencies for Perl distributions

%prep
%autosetup -n ExtUtils-MakeMaker-CPANfile-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR=%{buildroot}

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/ExtUtils/MakeMaker/CPANfile.pm
%{_mandir}/man3/ExtUtils::MakeMaker::CPANfile.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package fixed CPAN release and preserve its original default tests.
