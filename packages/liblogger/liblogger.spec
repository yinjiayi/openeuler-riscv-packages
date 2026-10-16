# SPDX-License-Identifier: Apache-2.0
Name:           liblogger
Version:        0.0.3
Release:        1%{?dist}
Summary:        Simple C console and file logging library
License:        MIT AND Apache-2.0
URL:            https://github.com/shinmorisawa/liblogger
Source0:        https://codeload.github.com/shinmorisawa/liblogger/tar.gz/1d68301a3288d5bd0ca49e9edf00f85184583e01#/liblogger-0.0.3.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt#/APACHE-2.0.txt
BuildRequires:  gcc make glibc-devel meson ninja-build bash coreutils
BuildRequires:  binutils rpm gzip tar grep gawk sed findutils diffutils patch

%description
A small C library for console and file logging. The original shared and
static builds are retained. Included downstream contract sources allow
installed replay; they are not an upstream test suite.

%package devel
Summary:        Development header for liblogger
Requires:       %{name} = %{version}-%{release}

%description devel
Public upstream liblogger header and installed-consumer contract sources.

%package static
Summary:        Static archive for liblogger
Requires:       %{name}-devel = %{version}-%{release}

%description static
The original default static library, without disabling the shared library.

%prep
%setup -q -n liblogger-1d68301a3288d5bd0ca49e9edf00f85184583e01
cp -p %{SOURCE1} APACHE-2.0.txt
# This is new downstream test code, not a replacement upstream source/test.
mkdir -p contract
cat > contract/consumer.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
#include <logger.h>
#include <stdlib.h>
#include <string.h>

#define CHECK(c) do { if (!(c)) abort(); } while (0)
int main(void) {
    const u8 levels[] = {LOGGER_LOG_TRACE, LOGGER_LOG_DEBUG, LOGGER_LOG_INFO,
        LOGGER_LOG_WARN, LOGGER_LOG_ERROR, LOGGER_LOG_FATAL, LOGGER_LOG_CATASTROPHIC};
    const char *markers[] = {"TRACE-one", "TRACE-two", "DEBUG-one", "DEBUG-two",
        "INFO-one", "INFO-two", "WARN-one", "WARN-two", "ERROR-one", "ERROR-two",
        "FATAL-one", "FATAL-two", "CATASTROPHIC-one", "CATASTROPHIC-two"};
    CHECK(strcmp(LOGGER_VERSION, "0.0.3") == 0);
    FILE *f = fopen("contract.log", "w");
    CHECK(f != NULL && fputs("existing-prefix\n", f) >= 0 && fclose(f) == 0);
    LoggerOptions opts = {0};
    opts.flags = LOGGER_FILE_LOG | LOGGER_CONSOLE_LOG | LOGGER_COLOR_ENABLE | LOGGER_ENABLE_SPLASH;
    opts.filename = "contract.log";
    opts.splash = "LOGGER-CONTRACT-SPLASH";
    Logger l = logger_init(opts);
    CHECK(l.result == OK && l.file != NULL);
    for (size_t i = 0; i < sizeof(levels) / sizeof(levels[0]); ++i) {
        logger_log(&l, levels[i], markers[2*i]);
        CHECK(l.result == OK && l.options.previous_log_type == levels[i]);
        logger_log(&l, levels[i], markers[2*i+1]);
        CHECK(l.result == OK && l.options.previous_log_type == levels[i]);
    }
    CHECK(logger_close(&l) == OK);
    f = fopen("contract.log", "rb");
    CHECK(f != NULL);
    char data[8192];
    size_t n = fread(data, 1, sizeof(data)-1, f);
    CHECK(!ferror(f) && feof(f) && fclose(f) == 0);
    data[n] = '\0';
    CHECK(strncmp(data, "existing-prefix\n", 16) == 0);
    CHECK(strstr(data, "LOGGER-CONTRACT-SPLASH") != NULL);
    CHECK(strchr(data, '\033') == NULL);
    for (size_t i = 0; i < sizeof(markers) / sizeof(markers[0]); ++i) {
        char *p = strstr(data, markers[i]);
        CHECK(p != NULL && strstr(p + strlen(markers[i]), markers[i]) == NULL);
    }
    opts = (LoggerOptions){0};
    opts.flags = LOGGER_CONSOLE_LOG;
    l = logger_init(opts);
    CHECK(l.result == OK && l.file == NULL);
    logger_log(&l, LOGGER_LOG_INFO, "plain-console");
    CHECK(logger_close(&l) == OK);
    opts = (LoggerOptions){0};
    opts.flags = LOGGER_FILE_LOG;
    l = logger_init(opts);
    CHECK(l.result == FILENAME_ERR && l.file == NULL);
    opts.filename = "nonexistent-contract-directory/log";
    l = logger_init(opts);
    CHECK(l.result == FOPEN_ERR && l.file == NULL);
    puts("LOGGER-CONTRACT-PASS");
    return 0;
}
C
cat > contract/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
prefix=${root%/}/usr
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() { rc=$?; if test "$rc" -eq 0; then rm -r -- "$work"; else printf 'Failed contract retained: %%s\n' "$work" >&2; fi; exit "$rc"; }
trap cleanup EXIT
cd "$work"
export LD_LIBRARY_PATH="$prefix/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cc -std=gnu11 -O2 -Wall -Wextra -Werror -UNDEBUG -I"$prefix/include/liblogger" "$self/consumer.c" -L"$prefix/lib64" -llogger -o shared-check
cc -std=gnu11 -O2 -Wall -Wextra -Werror -UNDEBUG -I"$prefix/include/liblogger" "$self/consumer.c" "$prefix/lib64/liblogger.a" -o static-check
for linkage in shared static; do
    "./$linkage-check" > "$linkage.out"
    test "$(grep -c '^LOGGER-CONTRACT-PASS$' "$linkage.out")" -eq 1
    grep -F 'LOGGER-CONTRACT-SPLASH' "$linkage.out"
    grep -F 'plain-console' "$linkage.out"
    for level in TRACE DEBUG INFO WARN ERROR FATAL CATASTROPHIC; do
        grep -F "$level-one" "$linkage.out"
        grep -F "$level-two" "$linkage.out"
    done
    grep -F $'\033[' "$linkage.out"
done
SH

%build
export CFLAGS="%{optflags}"
meson setup build --prefix=%{_prefix} --libdir=%{_libdir} --buildtype=plain
meson compile -C build -j2

%install
meson install -C build --destdir=%{buildroot} --no-rebuild
install -d %{buildroot}%{_datadir}/%{name}/tests
install -pm0644 contract/consumer.c %{buildroot}%{_datadir}/%{name}/tests/consumer.c
install -pm0755 contract/run-contract.sh %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh

%check
# No registered upstream tests in this release; keep the original invocation.
meson test -C build --no-rebuild --print-errorlogs
bash %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh %{buildroot}

%files
%license LICENSE APACHE-2.0.txt
%doc README.md DOCS.md
%{_libdir}/liblogger.so

%files devel
%license LICENSE APACHE-2.0.txt
%{_includedir}/liblogger/
%{_datadir}/%{name}/

%files static
%license LICENSE
%{_libdir}/liblogger.a

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.0.3-1
- Preserve original Meson shared/static defaults and add installed API replay.
