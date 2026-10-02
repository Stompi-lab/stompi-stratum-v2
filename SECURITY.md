# Security reporting

Report sensitive findings privately to the Stompi repository maintainer, using GitHub private vulnerability reporting where enabled. Do not include private keys, recovery words, RPC cookies or personal credentials in public issues.

See docs/VALIDATION.md for the scope of testing. The release has no independent audit claim. Upstream configurations contain fixed example/test keys; use scripts/stompi-config.py to create fresh local keys for your own pool. A native V2 miner must verify the pool's authority key. Monitoring metrics are not payment or blockchain-confirmation proofs.
