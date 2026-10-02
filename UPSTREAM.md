# Upstream provenance

This is a source snapshot with Stompi-specific modifications, not a repository with reconstructed upstream Git history.

- Application source: https://github.com/stratum-mining/sv2-apps
- Operator-reported checkout before local modifications: `9d7b18f113903f0efbb6904d32cede8adb778146`.
- Protocol dependency pinned by the uploaded Cargo.lock: https://github.com/stratum-mining/stratum at `28149a84d85fc3d0101202204c627389cb2d52ce`.
- External Template Provider used by the deployment: https://github.com/stratum-mining/sv2-template-provider at `b0b1833e7c250e7560430cd27872fce274a68619`.

The source snapshot was uploaded by the operator on 2026-10-02 after STP-address and Vardiff fixes were built and tested. Cargo.lock preserves dependency revisions; the uploaded snapshot itself has no .git directory.

Original licenses, authorship notices and documentation remain available. The former root README, contribution and release guides are preserved under docs/upstream. Original GitHub workflows are preserved as documentation in docs/upstream/github-workflows; they are not active release/notification automation in this fork. The new Stompi CI builds and tests the selected code paths without release publication or write permissions.

Stompi additions:
- STP payout/address parsing and targeted vectors.
- Pool-local work-weighted Vardiff and tests.
- Documentation, configuration generator, local generator tests and targeted CI.
- Reproduced external-provider CPU patch, including the const-method mutex correction.

The protocol, Noise transport and upstream application architecture are SRI work. Existing copyright and MIT/Apache notices are not replaced by the Stompi notice. New Stompi-specific code is Copyright (c) 2026 Stompi, MIT.
