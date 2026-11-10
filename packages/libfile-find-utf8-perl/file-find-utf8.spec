# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-find-utf8
Version:        0.016
Release:        1%{?dist}
Summary:        Find files with UTF-8-aware paths
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/File-Find-utf8
Source0:        File-Find-utf8-0.016.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(open)
Requires:       perl
Requires:       perl(File::Find)
Requires:       perl(Carp)
Requires:       perl(Encode)
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Find files with UTF-8-aware paths

%prep
%autosetup -n File-Find-utf8-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/Find/utf8.pm
%{_mandir}/man3/File::Find::utf8.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.016-1
- Package the fixed CPAN release and retain the original default tests.
