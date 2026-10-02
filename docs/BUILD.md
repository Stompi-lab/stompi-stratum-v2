# Build and run a Stompi V2 solo pool

## System prerequisites

The deployment described here used Ubuntu 24.04 x86_64, Rust 1.88.0, Cap'n Proto 1.0.1 and a Stompi Core IPC build. Install Rust/rustup separately if it is not present.

```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libssl-dev capnproto libcapnp-dev python3-cryptography
rustup toolchain install 1.88.0 --profile minimal
```

`capnproto` provides the compiler; `libcapnp-dev` provides `/usr/include/capnp/c++.capnp`, required by the Rust schema build scripts.

```bash
cargo test --locked -p pool_sv2 work_vardiff -j2
cargo test --locked -p stratum-apps --features pool stompi -j2
cargo test --locked -p stratum-apps --features pool payout -j2
python3 scripts/test_stompi_config.py
cargo build --release --locked -p pool_sv2 -j2
```

Keep `Cargo.lock` and use `--locked`. It records the exact protocol-library dependency commits. The five work-Vardiff tests exercise old job targets, mixed work, invalid work, window reset and stable 1.8 TH/s.

## Stompi node with IPC

Build Stompi Core with CMake `ENABLE_IPC=ON`, following the Core repository's build instructions. The IPC executable may retain the upstream name `bitcoin-node`; verify that it is built from Stompi source. Do not substitute an ordinary Bitcoin node.

Example, using locally installed Stompi binaries:

```bash
mkdir -p "$HOME/stompi-v2/node-data" "$HOME/stompi-v2/provider-data"
chmod 700 "$HOME/stompi-v2/node-data" "$HOME/stompi-v2/provider-data"
/path/to/stompi/bin/bitcoin-node \
  -datadir="$HOME/stompi-v2/node-data" \
  -daemon=0 -server=1 -ipcbind=unix \
  -listen=0 -connect=89.163.148.47:28333 \
  -rpcport=28432 -rpcbind=127.0.0.1
```

Run each component in its own terminal or supervised service. Wait until blocks equal headers and `initialblockdownload` is false:

```bash
/path/to/stompi/bin/stompi-cli \
  -datadir="$HOME/stompi-v2/node-data" -rpcport=28432 getblockchaininfo
```

Expected mainnet genesis:
`000000004ce46ead4546e107fc01668e9f3dafa15452a0766d9a03bc2167917b`.

## External Template Provider

The tested external source is https://github.com/stratum-mining/sv2-template-provider at commit `b0b1833e7c250e7560430cd27872fce274a68619`. It is a separate C++ project and is not bundled as a binary here. Follow that checkout's build prerequisites and CMake instructions.

```bash
git clone https://github.com/stratum-mining/sv2-template-provider.git
cd sv2-template-provider
git checkout b0b1833e7c250e7560430cd27872fce274a68619
patch --dry-run -p1 < /path/to/stompi-stratum-v2/patches/template-provider-cpu.patch
patch -p1 < /path/to/stompi-stratum-v2/patches/template-provider-cpu.patch
```

Build it and run its CTest suite before installation. The CPU patch stops polling idle sockets for writable events; it includes the `mutable` clients mutex needed by the const method. The tested deployment passed all seven provider tests after this change.

```bash
/path/to/sv2-tp \
  -conf=0 -datadir="$HOME/stompi-v2/provider-data" \
  -ipcconnect="unix:$HOME/stompi-v2/node-data/node.sock" \
  -sv2bind=127.0.0.1 -sv2port=18442
```

An optional mining-interface method may be unavailable on the tested v31 IPC node. The provider logs this compatibility fallback; verify that it subsequently connects, receives templates and serves the pool. RPC and Template Provider ports in this setup remain loopback-only.

## Generate your own pool configuration

From this repository, replace the CLI path and payout address with your own:

```bash
python3 scripts/stompi-config.py \
  --cli /path/to/stompi/bin/stompi-cli \
  --datadir "$HOME/stompi-v2/node-data" \
  --rpc-port 28432 \
  --address YOUR_OWN_STP_ADDRESS \
  --listen 0.0.0.0:3334 \
  --output stompi-pool.toml
```

This checks the Stompi mainnet genesis and validates the address through your node, then builds a `raw(...)` payout descriptor and creates fresh secp256k1 authority keys. It prints only the public key. The private configuration is created with mode 0600 and is never overwritten. The fallback payout address is used by the upstream donation mode; publish solo instructions so miners enter their own valid STP address. Arbitrary usernames may select donation mode in upstream behavior.

```bash
./target/release/pool_sv2 --config stompi-pool.toml
```

Permit TCP port 3334 through the relevant firewall if public mining is intended. Give miners your host, port, public pool key and the address-only username format. Keep `stompi-pool.toml` private. Do not use the fixed authority keys in upstream test configurations.

## Monitoring

```bash
curl -fsS http://127.0.0.1:19090/metrics
```

Upstream metrics expose connected clients, estimated hashrate, accepted/rejected shares and block solutions across current client channels. These are gauges and can decrease on disconnection or restart. They are not permanent accounting records or blockchain-confirmation proofs. This repository does not publish the private website/SSH collector used by the operator.
