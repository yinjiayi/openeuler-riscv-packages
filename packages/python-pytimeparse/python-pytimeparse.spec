# SPDX-License-Identifier: Apache-2.0
Name:           python-pytimeparse
Version:        1.1.9
Release:        1%{?dist}
Summary:        Parse human-readable time expressions in Python
License:        MIT
URL:            https://github.com/wroberts/pytimeparse
Source0:        pytimeparse-1.1.9-official.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-pynose

%description
Pytimeparse converts expressions of weeks, days, hours, minutes and seconds
to seconds, including fractional values, signs and day/clock formats.

%package -n python3-pytimeparse
Summary:        Parse human-readable time expressions in Python
Requires:       python3 >= 3.11

%description -n python3-pytimeparse
Pure Python time expression parser with the original upstream test modules.

%prep
%autosetup -n pytimeparse-c62ae66cbfc4a71b745a265842f179266391d953

%build
# Wheel ZIP timestamps cannot precede 1980; preserve later original epochs.
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
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} setup.py sdist bdist_wheel

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/pytimeparse-%{version}-py3-none-any.whl

%check
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
# Invoke the exact upstream test_suite entry point without setuptools fetching
# tests_require=['nose']; official pynose supplies that original nose module.
# Keep unfiltered collection of both test modules and the original doctest.
%{__python3} - <<'PY'
import os
import unittest
for key in list(os.environ):
    if key.startswith('NOSE_'):
        del os.environ[key]
os.environ['NOSE_IGNORE_CONFIG_FILES'] = '1'
from nose import collector
result = unittest.TextTestRunner(verbosity=2).run(collector())
assert result.testsRun == 57, ('incomplete upstream suite', result.testsRun)
assert result.wasSuccessful(), 'upstream suite failed'
assert not result.skipped, ('upstream tests skipped', result.skipped)
PY

%files -n python3-pytimeparse
%license LICENSE.rst
%doc README.rst
%{python3_sitelib}/pytimeparse/
%{python3_sitelib}/pytimeparse-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.9-1
- Onboard verified official release with complete original collector and doctest.
