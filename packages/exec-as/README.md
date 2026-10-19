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

The initial hosted target run failed the added shell-forwarding assertion.
The original check and earlier C-driver cases passed. Complete hexadecimal
argument observations, C child status 23 and direct-versus-exec-as shell
observations now precede the unchanged assertion. This is diagnostic input,
not a source fix, an accepted build or proof of a QEMU/native-only cause.

No source patch, disabled default test or local source/RPM/QEMU execution.
Repository validation is admission only: exact-head required CI, real target
build/ordinary installation and physical RPM/SRPM acceptance remain necessary.
