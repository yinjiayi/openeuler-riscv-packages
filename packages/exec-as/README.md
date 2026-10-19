# Exec-as

Exec-as 1.2.3 invokes a program using `execvp` with an explicit first argument
(`argv[0]`). Preserve the original default program and test build, and original
`make check` command without filtering. The full ISC notice and unchanged
source archive are retained in both explicit subpackages.

Staged and normally installed checks compile the unchanged original test
driver and repeat the original expected output. Added functional cases cover
custom names, spaces, empty arguments, PATH lookup, shell argument forwarding,
usage/missing/permission/directory errors and child exit status. These tests
do not establish native process timing, privileged execution, security
isolation or behavior of an empty argv array on other kernels.

The initial hosted target run failed an added shell-forwarding assertion,
while the original check and earlier C-driver cases passed. Target hexadecimal
argument observations confirmed that Exec-as preserved the process arguments.
For `sh -c command_string command_name argument`, POSIX defines shell `$0`
as `command_name`, independently of the process `argv[0]`. Retain the original
input with its specified output and add a case with an explicit shell name.
See https://pubs.opengroup.org/onlinepubs/9699919799/utilities/sh.html.
The argument diagnostics and C child status 23 checks remain. This corrects
the downstream test input/expectation, not upstream source; it does not establish
a QEMU/native-only cause or replace exact-head target acceptance.

No source patch, disabled default test or local source/RPM/QEMU execution.
Repository validation is admission only: exact-head required CI, real target
build/ordinary installation and physical RPM/SRPM acceptance remain necessary.
