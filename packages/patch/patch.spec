# SPDX-License-Identifier: Apache-2.0
Name:           patch
Version:        2.8
Release:        1%{?dist}
Summary:        Utility for applying diff files
License:        GPL-3.0-or-later
URL:            https://savannah.gnu.org/projects/patch/
Source0:        patch-%{version}.tar.xz

BuildRequires:  ed
BuildRequires:  gcc
BuildRequires:  libattr-devel
BuildRequires:  make
Requires:       ed

%description
GNU patch applies changes represented as context, unified, normal, or ed-style
diffs to original files.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc NEWS README
%{_bindir}/patch
%{_mandir}/man1/patch.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
