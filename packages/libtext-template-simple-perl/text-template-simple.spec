# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-template-simple
Version:        0.91
Release:        1%{?dist}
Summary:        Simple Perl text template engine and command line renderer
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Text-Template-Simple
Source0:        Text-Template-Simple-0.91.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Digest::MD5) >= 1
BuildRequires:  perl(CGI)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(Devel::Size) >= 0.77
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(lib)
Requires:       perl
Requires:       perl(Digest::MD5) >= 1
Requires:       perl(CGI)
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Fcntl)
Requires:       perl(File::Basename)
Requires:       perl(File::Find)
Requires:       perl(File::HomeDir)
Requires:       perl(File::Spec)
Requires:       perl(File::stat)
Requires:       perl(Getopt::Long)
Requires:       perl(IO::File)
Requires:       perl(Pod::Usage)
Requires:       perl(Safe)
Requires:       perl(Scalar::Util)
Requires:       perl(Symbol)
Requires:       perl(base)
Requires:       perl(constant)
Requires:       perl(overload)
Requires:       perl(strict)
Requires:       perl(subs)
Requires:       perl(vars)
Requires:       perl(warnings)

%description
Simple Perl text template engine and command line renderer

%prep
%autosetup -n Text-Template-Simple-%{version} -p1

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
%doc Changes TODO
%{_bindir}/tts
%{perl_vendorlib}/Text/Template/Simple.pm
%{perl_vendorlib}/Text/Template/Simple/
%{_mandir}/man1/tts.1*
%{_mandir}/man3/Text::Template::Simple*.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.91-1
- Package the fixed CPAN release with its unmodified default tests.
