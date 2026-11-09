# SPDX-License-Identifier: Apache-2.0
Name:           perl-config-file
Version:        1.54
Release:        1%{?dist}
Summary:        Parser for simple Perl configuration files
License:        GPL-2.0-or-later
URL:            https://metacpan.org/release/Config-File
Source0:        https://cpan.metacpan.org/authors/id/T/TH/THESEAL/Config-File-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(IO::File)
Requires:       perl(Carp)
Requires:       perl(Exporter)

%description
Read simple key/value configuration files in Perl, including comments,
variable substitution and nested keys.

%prep
%setup -q -n Config-File-%{version}

%build
perl Build.PL --installdirs vendor
./Build

%install
./Build install --destdir "%{buildroot}" --create_packlist 0

%check
perl -MTest::Pod -MTest::Pod::Coverage -e '1'
./Build test

%files
%license LICENSE
%doc README CHANGES
%{perl_vendorlib}/Config/File.pm
%{_mandir}/man3/Config::File.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.54-1
- Package the official release with its original functional and POD tests.
