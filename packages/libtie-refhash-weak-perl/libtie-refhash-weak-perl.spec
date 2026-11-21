# SPDX-License-Identifier: Apache-2.0
Name:           libtie-refhash-weak-perl
Version:        0.09
Release:        1%{?dist}
Summary:        Perl hashes with weak references as keys
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-RefHash-Weak
Source0:        Tie-RefHash-Weak-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Tie::RefHash) >= 1.34
BuildRequires:  perl(Variable::Magic)
BuildRequires:  perl(threads)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(B)
BuildRequires:  perl(overload)
BuildRequires:  perl(Exporter)
Requires:       perl
Requires:       perl(Scalar::Util)
Requires:       perl(Task::Weaken)
Requires:       perl(Tie::RefHash) >= 1.34
Requires:       perl(Variable::Magic)

%description
Tie::RefHash::Weak extends Tie::RefHash so a hash entry is released when
the last strong reference to its key goes out of scope.

%prep
%autosetup -n Tie-RefHash-Weak-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Keep all upstream defaults, including the original non-closure GC TODO.
make test TEST_VERBOSE=1

%files
%license Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes TODO
%{perl_vendorlib}/Tie/RefHash/Weak.pm
%{_mandir}/man3/Tie::RefHash::Weak.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package the official CPAN source with original tests and full license texts.
