# SPDX-License-Identifier: Apache-2.0
Name:           m4
Version:        1.4.21
Release:        1%{?dist}
Summary:        GNU macro processor
License:        GPL-3.0-or-later AND GFDL-1.3-or-later AND FSFULLR AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GPL-3.0-or-later WITH Texinfo-exception AND GPL-2.0-or-later WITH Autoconf-exception-generic AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND MIT
URL:            https://www.gnu.org/software/m4
Source0:        m4-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
GNU M4 is an implementation of the traditional Unix macro processor with
extensions commonly used by software build systems.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
# Gnulib's update-copyright test replaces init.sh's cleanup trap and can leave
# a root-owned mode-0700 test directory behind.  Make it traversable by the
# unprivileged artifact collector without changing any test result.
cleanup_test_permissions() {
    chmod -R a+rX tests/gt-test-update-copyright.sh.* 2>/dev/null || :
}
trap cleanup_test_permissions EXIT
make check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog ChangeLog-2014 NEWS README THANKS TODO
%{_bindir}/m4
%{_infodir}/m4.info*
%{_mandir}/man1/m4.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.21-1
- Initial openEuler RISC-V package based on Fedora 44 and corroborating release evidence.
