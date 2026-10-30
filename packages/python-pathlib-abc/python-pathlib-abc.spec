# SPDX-License-Identifier: Apache-2.0
Name:           python-pathlib-abc
Version:        0.5.2
Release:        1%{?dist}
Summary:        Abstract base classes for virtual filesystem paths
License:        PSF-2.0
URL:            https://github.com/barneygale/pathlib-abc
Source0:        pathlib_abc-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-pytest

%description
Pathlib-abc provides JoinablePath, ReadablePath and WritablePath abstract base
classes for implementing pathlib-like virtual filesystem paths.

%package -n python3-pathlib-abc
Summary:        Abstract base classes for virtual filesystem paths
Requires:       python3 >= 3.9

%description -n python3-pathlib-abc
Abstract base classes and protocols for pathlib-like virtual filesystem paths.

%prep
%autosetup -n pathlib_abc-%{version}

%build
# Wheel ZIP timestamps cannot precede 1980-01-01 UTC. Only raise earlier epochs.
source_date_epoch=${SOURCE_DATE_EPOCH-0}
case "$source_date_epoch" in
  ''|*[!0-9]*)
    printf '%s\n' 'SOURCE_DATE_EPOCH must be a nonnegative decimal integer' >&2
    exit 1
    ;;
esac
epoch_compare=$source_date_epoch
while [ "${epoch_compare#0}" != "$epoch_compare" ]; do
  epoch_compare=${epoch_compare#0}
done
epoch_compare=${epoch_compare:-0}
if [ "${#epoch_compare}" -lt 9 ] || \
   { [ "${#epoch_compare}" -eq 9 ] && [ "$epoch_compare" -lt 315532800 ]; }; then
  SOURCE_DATE_EPOCH=315532800
else
  SOURCE_DATE_EPOCH=$source_date_epoch
fi
export SOURCE_DATE_EPOCH
printf '%s\n' "Wheel build SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH"
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip wheel --no-build-isolation --no-deps --wheel-dir dist .

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/pathlib_abc-%{version}-py3-none-any.whl

%check
# Preserve upstream tox's default command and encoding-warning environment.
export PYTHONWARNDEFAULTENCODING=1
%{__python3} -m pytest tests

%files -n python3-pathlib-abc
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{python3_sitelib}/pathlib_abc/
%{python3_sitelib}/pathlib_abc-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.2-1
- Onboard verified official sdist with complete unchanged default pytest suite.
