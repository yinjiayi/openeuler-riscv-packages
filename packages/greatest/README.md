# Greatest 1.5.0

Official stable v1.5.0 resolves to commit
11a6af1919049df502405913da64fb385c219361. Archive SHA-256:
e1ddc85dc4892318993e0dee0acf891a123eeff9748c549cc19d5387d73b98e1.
All 18 original Git files/modes match the fixed archive. ISC LICENSE is
shipped in both RPMs; no upstream patch, generated binary or ELF is installed.

The main RPM installs greatest.h. greatest-tests installs the original
Makefile and seven C/C++ example inputs. Original make all builds all five
C programs; all_cpp adds the original C++ program. Their warning flags,
default language modes and complete default cases are preserved.

A negative-example oracle means independently derived expected counts and
exit codes, not ignored errors. Five examples intentionally fail or skip
cases. Each default program runs with no filtering/seed/verbosity options.
The main example's fixed C99-or-later cases are 9 passes,20 failures,2 skips;
its 200 random cases are predicted by a separate stdlib-only process with
the same target libc default rand sequence, without including greatest.h,
reseeding or interposing symbols. Exact totals and exits must match. Its
full slow Fibonacci cases through39 remain enabled. Other exact
(pass,fail,skip; exit) outcomes are no_suite(1,1,1;1),
no_runner(1,0,0;0),shuffle(1064,2,0;1),trunc(11,0,0;0),cpp(0,1,0;1).
These are framework-reporting tests, not an all-pass or zero-skip claim.

%check repeats every original default program against the source header and
the staged installed header. Smoke verifies both RPMs, then recompiles and
repeats all defaults against the actual installed header. All target work
runs in CI's locked openEuler24.03 LTS SP3/riscv64/RVA23 image, not locally.
Timing in upstream output is not native performance evidence.

Historical AUR1.5.0-1 metadata establishes component discovery only; it was
marked stale in the repository's original snapshot. Fixed official release,
license, test and current target supplier checks are independent admission
requirements; no AUR recipe is executed.
