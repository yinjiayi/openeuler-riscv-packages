# SPDX-License-Identifier: Apache-2.0
Name:           ccd2cue
Version:        0.5
Release:        1%{?dist}
Summary:        Convert CloneCD cuesheets (.ccd) to less-compatible CDRWIN cuesheets (.cue)
License:        GPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://www.gnu.org/software/ccd2cue/
Source0:        ccd2cue-0.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Convert CloneCD cuesheets (.ccd) to less-compatible CDRWIN cuesheets (.cue)

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
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_infodir}/ccd2cue.info*
%{_mandir}/man1/ccd2cue.1*
%{_mandir}/*/man1/ccd2cue.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5-1
- Initial openEuler RISC-V package from the full package inventory.
