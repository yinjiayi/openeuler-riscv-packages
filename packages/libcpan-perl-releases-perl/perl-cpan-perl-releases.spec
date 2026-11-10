# SPDX-License-Identifier: Apache-2.0
Name:           perl-cpan-perl-releases
Version:        5.20261022
Release:        1%{?dist}
Summary:        Map Perl releases to CPAN tarball locations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/CPAN-Perl-Releases
Source0:        CPAN-Perl-Releases-5.20261022.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6.0
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(vars)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.47
Requires:       perl >= 5.6.0
Requires:       perl(Exporter)
Requires:       perl(vars)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Map Perl releases to CPAN tarball locations

%prep
%autosetup -n CPAN-Perl-Releases-%{version} -p1
# Preserve generator attribution with the complete original license.
cat > TEMPLATE-NOTICES <<'NOTICE'
Dist::Zilla generated portions: Ricardo SIGNES and contributors.
Dist::Zilla::Plugin::Test::Compile: Jérôme Quelin and contributors.
The generator distributions grant redistribution under the same terms
as Perl itself. Their exact release and file provenance is in the recipe
README. The complete GNU GPL and Artistic terms are retained in LICENSE.
NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE TEMPLATE-NOTICES
%doc README Changes
%{perl_vendorlib}/CPAN/Perl/Releases.pm
%{_mandir}/man3/CPAN::Perl::Releases.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.20261022-1
- Package the fixed upstream release with its original default suite.
