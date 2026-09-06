# SPDX-License-Identifier: Apache-2.0
Name:           macchanger
Version:        1.7.0
Release:        1%{?dist}
Summary:        Utility for changing network interface MAC addresses
License:        GPL-3.0-or-later
URL:            https://github.com/alobbs/macchanger
Source0:        macchanger-1.7.0.tar.gz
Patch0:         0001-doc-drop-missing-gpl-texi-input.patch
Patch1:         0002-prefer-urandom-seed-source.patch
Patch2:         0003-check-random-seed-and-fix-size-format.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  texinfo

%description
macchanger displays and changes the MAC address of a network interface.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
./src/macchanger --version | grep -F '%{version}'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/macchanger
%{_datadir}/macchanger/
%{_mandir}/man1/macchanger.1*
%{_infodir}/macchanger.info*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.0-1
- Initial openEuler RISC-V package.
