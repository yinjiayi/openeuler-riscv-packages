# SPDX-License-Identifier: Apache-2.0
Name:           diffutils
Version:        3.12
Release:        1%{?dist}
Summary:        GNU utilities for comparing text files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/diffutils/
Source0:        diffutils-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  perl

%description
GNU diffutils provides diff, cmp, diff3, and sdiff for comparing and merging
text files.

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
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README THANKS
%{_bindir}/cmp
%{_bindir}/diff
%{_bindir}/diff3
%{_bindir}/sdiff
%{_mandir}/man1/cmp.1*
%{_mandir}/man1/diff.1*
%{_mandir}/man1/diff3.1*
%{_mandir}/man1/sdiff.1*
%{_infodir}/diffutils.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.12-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
