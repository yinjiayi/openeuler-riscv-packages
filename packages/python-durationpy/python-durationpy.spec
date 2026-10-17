# SPDX-License-Identifier: Apache-2.0
Name:           python-durationpy
Version:        0.11
Release:        1%{?dist}
Summary:        Parse and format Go duration strings as Python timedeltas
License:        MIT
URL:            https://github.com/icholy/durationpy
Source0:        durationpy-0.11-official.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip

%description
Durationpy converts Go duration strings to Python datetime.timedelta objects
and formats timedeltas as ordinary or extended duration strings.

%package -n python3-durationpy
Summary:        Parse and format Go duration strings as Python timedeltas
Requires:       python3

%description -n python3-durationpy
Pure Python duration conversion library, including its original typing stubs.

%prep
%autosetup -n durationpy-3df7a337a852f0b432f73c4892c4b48590a01bd0

%build
# ZIP timestamps cannot precede 1980; raise only earlier nonnegative epochs.
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
# Preserve the original mise build command; neither step fetches dependencies.
%{__python3} setup.py sdist bdist_wheel

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/durationpy-%{version}-py3-none-any.whl

%check
# Complete original fixed-release unittest suite, without filters or skips.
%{__python3} test.py

%files -n python3-durationpy
%license LICENSE
%doc README.md
%{python3_sitelib}/durationpy/
%{python3_sitelib}/durationpy-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Onboard complete verified official release source and unchanged unittest suite.
