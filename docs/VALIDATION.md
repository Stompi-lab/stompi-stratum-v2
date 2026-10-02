# Validation record — 2026-10-02

## Operator-reported build and runtime evidence

These checks ran on the operator's Ubuntu 24.04 x86_64 deployment, before packaging:

- Five pool-local work-Vardiff tests passed after correcting the mixed-work test baseline to cross the existing update threshold.
- Nineteen payout tests passed, including Stompi solo payout and rejection of invalid STP identities.
- Two Stompi-specific filtered tests passed during the address-parser build.
- `cargo build --release --locked -p pool_sv2 -j2` succeeded; the supervised pool restarted successfully.
- A native-V2 Bitaxe connected and produced accepted extended-channel shares.
- Runtime share difficulty stabilized in the low thousands for an approximately 1.8 TH/s miner, instead of the earlier runaway estimate. The device reported approximately 4,408 at the later check.
- The external Template Provider passed seven CTest tests after its idle-socket CPU patch. Runtime CPU fell from roughly one saturated thread to approximately 0.1% for that thread during the reported observation.

Stompi mainnet solo reward evidence:

- Block 19024: `0000000000000b2e8b6b9791496f53939c6e60b869fcdec2e11297012ea36ecc`, 50 STP coinbase output, independently observed by the main node.
- Block 19035: `0000000000000ea7b03d60276790198bb0ecf5c8b43112e97ab8977af4128d97`, coinbase transaction `2de2f11e38f04f5aed7bc9ed5551b2dadb1a7308d99117f4f814a137cd0c3f3d`, 50 STP to the miner's selected second wallet, two confirmations in the main-node output supplied at the time.

This is a dated operator evidence record, not a fresh remote chain query or an independent security audit.

## Packaging checks

- Uploaded corrected test baseline and Stompi code paths inspected.
- Three new configuration-generator tests executed locally: public/private codec correspondence, raw versus JSON RPC parsing, and mode-0600/no-overwrite file behavior.
- Provider CPU patch dry-run checked against uploaded original files; both header and source changes apply together.
- Main examples and scripts checked for obvious credential patterns and accidental live configuration inclusion.
- No productive authority keys or SSH credentials were identified in the uploaded source tree. Upstream fixed example/test authority keys remain public test fixtures and are documented as unsuitable for deployment.
- New CI and docs are provided; their first GitHub run has not yet occurred.

Rust was not available in the packaging environment. The complete package was not freshly compiled there. The new generator and documentation do not alter the tested payout or Vardiff implementation. Remaining upstream integration tests and other roles are not claimed to be validated for Stompi.
