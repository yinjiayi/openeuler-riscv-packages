# Golden acceptance fixtures

A golden package is a fixed acceptance sample whose source bytes, expected state, allowed changes, and decisive evidence are versioned here. It is not evidence about the rest of the catalog.

The inline-assembly case has two observable stages. **Baseline** means the PR head does not contain the declared target patch; that head must fail on RISC-V and classify as `repair-queued`. **Repaired** means the same PR branch contains the exact package-local repair; the latest head must pass. `scripts/golden-eval evaluate --stage auto` selects between those stages from the declared target-patch path. It never treats a prior run, a synthetic result, or an old commit as evidence for the current head.

The native-kernel fixture only validates routing. `needs-native-riscv` is a blocked validation state, not a successful QEMU build. No patch or Auto-merge is allowed until an independently approved native RISC-V runner exists.

Fixture archives are generated with sorted entries, normalized ownership and modes, zero mtimes, and deterministic gzip metadata. The manifests pin both the input-tree digest and canonical archive digest; generated tarballs are evidence artifacts and are not committed.
