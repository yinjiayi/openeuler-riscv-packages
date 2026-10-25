# SPDX-License-Identifier: Apache-2.0
Name:           bchunk
Version:        1.2.2
Release:        1%{?dist}
Summary:        Convert BIN/CUE CD images to ISO, CDR and WAV tracks
License:        GPL-2.0-or-later
URL:            https://github.com/hessu/bchunk
Source0:        bchunk-1.2.2-0c7009d.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  python3

# Explicit runtime QA dependencies for the committed installed smoke test.
# The converter itself only needs its ordinary auto-generated ELF requires.
Requires:       bash
Requires:       python3

%description
BinChunker converts BIN/CUE CD image files into ISO data tracks, raw CDR
audio tracks, or WAV audio tracks without accessing an optical device.

%prep
%autosetup -n hessu-bchunk-0c7009d -p1

%build
# Preserve the original default all target and all conversion features.
# Command-line variables override upstream assignments without source edits.
%make_build CC="%{__cc}" LD="%{__cc}" \
    CFLAGS="%{optflags} -Wall -Wstrict-prototypes" \
    LDFLAGS="%{?build_ldflags}" all

%install
# Preserve both upstream products without install's ownership/strip actions.
install -Dpm 0755 bchunk %{buildroot}%{_bindir}/bchunk
install -Dpm 0644 bchunk.1 %{buildroot}%{_mandir}/man1/bchunk.1

%check
# Complete seven-file upstream source has no tests/check target or test suite.
# These are added packaging regression cases, not substituted upstream tests.
python3 -I - "$PWD/bchunk" <<'PY'
import os
import pathlib
import struct
import subprocess
import sys
import tempfile

binary = pathlib.Path(sys.argv[1]).resolve(strict=True)
if not binary.is_file() or not os.access(binary, os.X_OK):
    raise SystemExit("bchunk executable missing")

def require(ok, message):
    if not ok:
        raise SystemExit(message)

def swap_audio(data):
    result = bytearray(data)
    result[0::2], result[1::2] = data[1::2], data[0::2]
    return bytes(result)

def wave(data):
    return struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", len(data) + 36,
                       b"WAVE", b"fmt ", 16, 1, 2, 44100, 176400,
                       4, 16, b"data", len(data)) + data

def cue(tracks, newline="\n"):
    lines = ['FILE "image.bin" BINARY']
    for number, mode, frame in tracks:
        lines += [f"  TRACK {number:02d} {mode}",
                  f"    INDEX 01 00:00:{frame:02d}"]
    return (newline.join(lines) + newline).encode("ascii")

sectors = [bytes((73 * i + 29 * sector + 11) & 255
                 for i in range(2352)) for sector in range(3)]
image = b"".join(sectors)

with tempfile.TemporaryDirectory(prefix="bchunk-qa-") as directory:
    root = pathlib.Path(directory)

    def invoke(case, args, expected_status=0):
        result = subprocess.run([str(binary), *args], cwd=case,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"},
                                timeout=30, check=False)
        require(result.returncode == expected_status,
                f"{case.name}: exit {result.returncode}, expected {expected_status}; "
                f"stdout={result.stdout!r} stderr={result.stderr!r}")
        require(b"binchunker for Unix, version 1.2.2 by " in result.stdout,
                f"{case.name}: wrong version banner")
        return result

    def conversion(name, options, tracks, expected, newline="\n"):
        case = root / name
        case.mkdir()
        (case / "image.bin").write_bytes(image)
        (case / "image.cue").write_bytes(cue(tracks, newline))
        invoke(case, [*options, "image.bin", "image.cue", "out"])
        actual = {item.name: item.read_bytes() for item in case.iterdir()
                  if item.name.startswith("out")}
        require(actual == expected, f"{name}: output names/bytes differ")

    m1 = b"".join(sector[16:2064] for sector in sectors)
    m2 = b"".join(sector[24:2072] for sector in sectors)
    psx = b"".join(sector[:2336] for sector in sectors)
    m2336 = b"".join(sector[16:] for sector in sectors)
    conversion("mode1", [], [(1, "MODE1/2352", 0)], {"out01.iso": m1})
    conversion("mode1-verbose", ["-v"], [(1, "MODE1/2352", 0)], {"out01.iso": m1})
    conversion("mode1-crlf", [], [(1, "MODE1/2352", 0)], {"out01.iso": m1}, "\r\n")
    conversion("mode2", [], [(1, "MODE2/2352", 0)], {"out01.iso": m2})
    conversion("mode2-raw", ["-r"], [(1, "MODE2/2352", 0)], {"out01.iso": image})
    conversion("mode2-psx", ["-p"], [(1, "MODE2/2352", 0)], {"out01.iso": psx})
    conversion("mode2-raw-precedence", ["-p", "-r"], [(1, "MODE2/2352", 0)], {"out01.iso": image})
    conversion("mode2-2336", [], [(1, "MODE2/2336", 0)], {"out01.iso": m2336})
    conversion("audio", [], [(1, "AUDIO", 0)], {"out01.cdr": image})
    conversion("audio-swap", ["-s"], [(1, "AUDIO", 0)], {"out01.cdr": swap_audio(image)})
    conversion("audio-wave", ["-w"], [(1, "AUDIO", 0)], {"out01.wav": wave(image)})
    conversion("audio-wave-swap", ["-w", "-s"], [(1, "AUDIO", 0)], {"out01.wav": wave(swap_audio(image))})
    conversion("unknown-mode", [], [(1, "UNRECOGNIZED", 0)], {"out01.ugh": image})
    conversion("mixed-tracks", [], [(1, "MODE1/2352", 0), (2, "AUDIO", 1)],
               {"out01.iso": sectors[0][16:2064], "out02.cdr": sectors[1] + sectors[2]})
    conversion("audio-wave-tracks", ["-w"], [(1, "AUDIO", 0), (2, "AUDIO", 2)],
               {"out01.wav": wave(sectors[0] + sectors[1]), "out02.wav": wave(sectors[2])})

    case = root / "cli"
    case.mkdir()
    result = invoke(case, ["-h"])
    require(b"Usage: bchunk" in result.stderr, "help: missing usage")
    result = invoke(case, [], 1)
    require(b"Usage: bchunk" in result.stderr, "missing-args: missing usage")
    (case / "image.bin").write_bytes(image)
    (case / "image.cue").write_bytes(cue([(1, "MODE1/2352", 0)]))
    result = invoke(case, ["missing.bin", "image.cue", "out"], 2)
    require(b"Could not open BIN" in result.stderr, "missing-bin: wrong diagnostic")
    result = invoke(case, ["image.bin", "missing.cue", "out"], 2)
    require(b"Could not open CUE" in result.stderr, "missing-cue: wrong diagnostic")
    (case / "empty.cue").write_bytes(b"")
    result = invoke(case, ["image.bin", "empty.cue", "out"], 3)
    require(b"Could not read first line" in result.stderr, "empty-cue: wrong diagnostic")
    (case / "bad.cue").write_bytes(b'FILE "image.bin" BINARY\nTRACK\n')
    result = invoke(case, ["image.bin", "bad.cue", "out"], 3)
    require(b"no space after TRACK" in result.stderr, "bad-track: wrong diagnostic")
    require(not any(item.name.startswith("out") for item in case.iterdir()),
            "CLI/error cases unexpectedly created output tracks")

print("bchunk packaging QA: 15 conversions and 6 CLI/error cases passed")
PY

%files
%license COPYING
%doc README ChangeLog
%{_bindir}/bchunk
%{_mandir}/man1/bchunk.1*

%changelog
* Fri Oct 23 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Static draft preserving the fixed upstream release and all default features.
- Add byte-exact conversion and CLI regressions for build and installed QA.
