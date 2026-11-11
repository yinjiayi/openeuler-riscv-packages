# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-Callback
Version:        2.00
Release:        1%{?dist}
Summary:        Filehandles backed by Perl callbacks
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Callback
Source0:        IO-Callback-2.00.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(IO::String)
BuildArch:      noarch

%description
Filehandles backed by Perl callbacks

%prep
%autosetup -p1 -n IO-Callback-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/IO/Callback.pm
%{_mandir}/man3/IO::Callback.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.00-1
- Package IO::Callback with its original test suite.
