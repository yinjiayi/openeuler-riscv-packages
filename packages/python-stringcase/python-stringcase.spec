# SPDX-License-Identifier: Apache-2.0
Name:           python-stringcase
Version:        1.2.0
Release:        1%{?dist}
Summary:        Convert strings between common naming conventions
License:        MIT
URL:            https://github.com/okunishinishi/python-stringcase
Source0:        stringcase-1.2.0-official.tar.gz
Patch0:         0001-normalize-alphanumcase-input.patch
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-coverage

%description
Stringcase converts strings between camel, Pascal, snake, spinal, path, title
and other naming conventions. The source includes the complete upstream tests.

%package -n python3-stringcase
Summary:        Convert strings between common naming conventions
Requires:       python3 >= 3.11
Requires:       python3-coverage

%description -n python3-stringcase
Pure Python string case conversion and the unchanged original unittest suite
for installed-package acceptance.

%prep
%autosetup -p1 -n python-stringcase-be60b723753d4796983729d49ef825826e0f882d

%build
# ZIP wheel timestamps have a 1980 lower bound. Preserve later RPM epochs.
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
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
# Unmodified distutils setup; target setuptools supplies the legacy wheel backend.
%{__python3} -m pip wheel --no-index --no-deps --no-build-isolation \
    --wheel-dir dist .

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/stringcase-%{version}-py3-none-any.whl
install -d %{buildroot}%{_datadir}/python-stringcase/test
install -m 0644 stringcase_test.py %{buildroot}%{_datadir}/python-stringcase/test/

%check
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
# Never consume the tracked historical .coverage file from the official source.
check_dir=$(mktemp -d "$PWD/rpm-check.XXXXXXXX")
export COVERAGE_FILE="$check_dir/.coverage"
# Original Travis defaults, no selection, exclusions or ignored failures.
%{__python3} -m unittest -v stringcase_test.py
%{__python3} -m coverage run -m unittest stringcase_test
%{__python3} -m coverage html -d docs/report/coverage/
# Additional completeness gate; all original tests remain in the suite.
%{__python3} - <<'PY'
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('stringcase_test')
assert suite.countTestCases() == 13, 'incomplete original suite'
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun == 13 and result.wasSuccessful() and not result.skipped
PY

%files -n python3-stringcase
%license LICENSE
%doc README.rst
%{python3_sitelib}/stringcase.py
%{python3_sitelib}/__pycache__/stringcase.*.pyc
%{python3_sitelib}/stringcase-%{version}.dist-info/
%{_datadir}/python-stringcase/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Onboard fixed release-associated official source and retain original test defaults.
- Normalize alphanumcase input to honor the original None test without exclusions.
