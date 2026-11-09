# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-noplan
Version:        0.0.6
Release:        1%{?dist}
Summary:        Check that Perl tests do not use no_plan
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-NoPlan
Source0:        Test-NoPlan-v0.0.6.tar.gz
Source1:        Module-Build-0.3603.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Carp)
BuildRequires:  perl(version)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.22
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Pod::Coverage) >= 0.18
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Pod::Find)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(base)
Requires:       perl(Exporter)
Requires:       perl(Test::Builder::Module)
Requires:       perl(FindBin)
Requires:       perl(Cwd)
Requires:       perl(File::Spec)
Requires:       perl(Carp)
Requires:       perl(version)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::NoPlan inspects Perl test files for explicit no_plan usage.
It provides a file checker and a directory-wide test assertion.

%prep
%autosetup -n Test-NoPlan-v%{version} -p1
# Retain the original copyright and grant for the unused generated wrapper.
tar -xOzf "%{SOURCE1}" Module-Build-0.3603/lib/Module/Build/Compat.pm \
    | %{__perl} -0777 -ne 'print $1 if /(^=head1 COPYRIGHT\n.*?)(?=^=head1 )/ms' \
    > NOTICE.Module-Build-Compat
test -s NOTICE.Module-Build-Compat

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --create_packlist=0 --destdir "%{buildroot}"

%check
%{__perl} Build test --verbose

%files
%license README NOTICE.Module-Build-Compat
%doc AUTHORS Changes
%{perl_vendorlib}/Test/NoPlan.pm
%{_mandir}/man3/Test::NoPlan.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-1
- Package Test::NoPlan with the original default tests and generated-wrapper notice.
