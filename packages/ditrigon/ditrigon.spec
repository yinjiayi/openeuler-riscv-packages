# SPDX-License-Identifier: Apache-2.0
Name:           ditrigon
Version:        1.6.0
Release:        4%{?dist}
Summary:        A popular and easy to use graphical IRC (chat) client
License:        GPL-2.0-or-later
URL:            https://github.com/bluewww/ditrigon
Source0:        ditrigon-1.6.0.tar.gz
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libappstream-glib
BuildRequires:  libcanberra-devel
BuildRequires:  luajit-devel
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  pciutils-devel
BuildRequires:  perl-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-devel

%description
A popular and easy to use graphical IRC (chat) client

%prep
%autosetup -p1

%build
%meson \
  -Dgtk4-frontend=true \
  -Dtls=enabled \
  -Dplugin=true \
  -Ddbus=enabled \
  -Dlibcanberra=enabled \
  -Dinstall-appdata=true \
  -Dwith-checksum=true \
  -Dwith-fishlim=true \
  -Dwith-lua=luajit \
  -Dwith-perl=perl \
  -Dwith-python=python3 \
  -Dwith-sysinfo=true
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING


%changelog
* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-4
- Declare python3-cffi for the enabled Python plugin generator.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-3
- Declare Doxygen so the enabled API documentation target can be configured.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-2
- Declare the development dependencies for the GTK 4 client and plugins.
- Keep TLS, DBus, sound integration, and the default plugin set enabled.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
