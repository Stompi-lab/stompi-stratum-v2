# Stompi Stratum V2

Stratum V2 solo mining for the Stompi proof-of-work network. Based on the Stratum V2 Reference Implementation (SRI) `sv2-apps`, with Stompi payout addresses and accepted-work-based variable difficulty.

[Deutsch](README-DE.md) · [Build and operation](docs/BUILD.md) · [Validation](docs/VALIDATION.md) · [Upstream provenance](UPSTREAM.md)

## Features

- Native Stratum V2 mining with Noise transport and pool authority keys.
- Stompi `stp1…` payout addresses, including bare address usernames and optional `.worker` suffixes.
- Solo block rewards paid directly in the coinbase to the miner's address.
- Work-weighted Vardiff: rejected shares do not count, and old jobs retain their own accepted share difficulty.
- Upstream Prometheus monitoring, bound to localhost by the example configuration.
- A local configuration generator that validates the Stompi network and payout address and generates fresh authority keys.

This repository contains source, configuration examples and build instructions. It does not include a live pool's private configuration, wallet keys, website, server administration or private SSH credentials. Internal upstream names such as `bitcoin-core-sv2` are retained for compatibility and provenance.

## Public pool

| Setting | V1 | V2 |
| --- | --- | --- |
| Host | `v1.stompi.tech` | `v2.stompi.tech` |
| Port | `3333` | `3334` |
| Username | Your own STP address | Your own STP address |
| Optional worker | `STP_ADDRESS.worker` | `STP_ADDRESS.worker` |
| Password | `x` | Follow the native V2 miner UI |

Public V2 authority key (deployment documented on 2026-10-02):

```text
9bekteT2vX3aA7AvBXVMtCv6dMFoDMZvgb7Yfv95Q3aXgsTRuM9
```

Select native Stratum V2 in the miner and configure the authority key. A V1-only miner needs a translator; the translator is part of upstream source but has not been validated on Stompi in this release. These hostnames are mining endpoints, not separate HTTPS pool websites. Pool information: https://stompi.tech/#/pool.

## Quick build

With Rust/rustup and the system prerequisites installed:

```bash
rustup toolchain install 1.88.0 --profile minimal
cargo test --locked -p pool_sv2 work_vardiff -j2
cargo test --locked -p stratum-apps --features pool stompi -j2
cargo test --locked -p stratum-apps --features pool payout -j2
cargo build --release --locked -p pool_sv2 -j2
```

See [docs/BUILD.md](docs/BUILD.md) for prerequisites, the Stompi IPC node, the external Template Provider, and creation of a private configuration. Starting a pool requires those components; compiling `pool_sv2` alone is not a complete node installation.

## Scope and validation

The Stompi code paths have targeted test coverage and a native-V2 Bitaxe mining deployment with confirmed Stompi mainnet blocks. The uploaded Vardiff code passed five tests and the payout suite passed nineteen tests on the operator's server. This source package is not an independently audited release; other upstream roles and Bitcoin integration tests are not claimed to be Stompi-validated. Pool share difficulty does not change the chain's ten-minute target or consensus rules.

## Licenses

Upstream code retains its MIT/Apache-2.0 licensing and existing notices. Stompi-specific additions: Copyright (c) 2026 Stompi, MIT. See [LICENSE.md](LICENSE.md), [LICENSE-STOMPI](LICENSE-STOMPI) and [UPSTREAM.md](UPSTREAM.md).
