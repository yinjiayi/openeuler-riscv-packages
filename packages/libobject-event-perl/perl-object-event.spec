# SPDX-License-Identifier: Apache-2.0
Name:           perl-object-event
Version:        1.101
Release:        1%{?dist}
Summary:        Register callbacks and dispatch events on Perl objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Object-Event
Source0:        Object-Event-1.101.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(AnyEvent) >= 3.5
BuildRequires:  perl(AnyEvent::Util)
BuildRequires:  perl(common::sense)
BuildRequires:  perl(Carp)
BuildRequires:  perl(sort)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(AnyEvent) >= 3.5
Requires:       perl(AnyEvent::Util)
Requires:       perl(common::sense)
Requires:       perl(Carp)
Requires:       perl(sort)

%description
Object::Event lets Perl objects register callbacks, assign them priorities,
and dispatch events to those callbacks.

%prep
%autosetup -n Object-Event-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Object/Event.pm
%{_mandir}/man3/Object::Event.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.23-1
- Package Object::Event 1.23 with its original default tests.
