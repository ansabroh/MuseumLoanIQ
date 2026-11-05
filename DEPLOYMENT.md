# Deployment and validation

## Final deployment

- Network: GenLayer Studionet, chain ID **61999**.
- RPC: `https://studio.genlayer.com/api`.
- Contract: `0xE6cc276002756C3F1123AD4Ce5d212eAf574D331`.
- Explorer: https://explorer-studio.genlayer.com/address/0xE6cc276002756C3F1123AD4Ce5d212eAf574D331
- Deployment transaction: `0x85c35934beb5a19a72e92a38b632db2c1a9e10d1be6c2ff6473a02691d0dae62`.
- Deployed through Studio's built-in account: `0x17f4AC81CDb3A2cF1093970e255c1a6590C7F7F7`.
- Full-consensus NORMAL execution, not leader-only.
- Runtime dependency is pinned in the first source line. `evidence/source-verification.json` records the deployed code SHA-256 and exact source comparison.

An earlier SDK connectivity deployment exists at `0xD855E57bE97370D3419f48375d44792B078d0FBD`; it is not the dashboard's final contract. The dashboard points only to the final built-in-account deployment above.

## Live lifecycle

The demonstration `museum-demo-001` ran register → borrower acceptance → commit evidence → assess, followed by two append-only evidence revisions. Its three finalized assessments are COMPLIANT, REVIEW_REQUIRED and NONCOMPLIANT. They exercise real pinned HTTP retrieval and real independent AI validator consensus; no LLM mocks or fabricated final results were used in these live transactions.

`evidence/verified-receipts.json` contains the final deployment, eight lifecycle writes and a separate frontend-origin registration, with hashes, execution results, votes and nondeterministic outputs when returned by the RPC. `evidence/live-loan.json` is the exported on-chain record. The public test identities used by `scripts/live-smoke.mjs` are intentionally disposable and must never hold funds.

The separate browser registration `dashboard-live-001` was submitted by a locally created Studio-style signer and visibly completed the frontend's pending → finalized → successful state refresh. Hash: `0x3f831c783c9b5fac030f91f91759c7ab9512e493630b6b423414162eab1c40db`.

## Checks

- 21 SDK direct-mode tests: semantic outcomes, validator agreement/dissent, numeric breaches, coverage gaps, ungrounded quotes, authorization, immutable terms, URL pinning, hash mismatch, identity mismatch, invalid units/order, and receipt-chain preservation.
- 8 JavaScript lifecycle tests: accepted vs final state, failure vs execution success, real/numeric Studio receipt shapes and timeout without duplicate writes.
- GenVM lint/schema: passed; six methods (four write, two view).
- Vite production build: passed.
- Browser: desktop layout inspected, account creation verified and real frontend write completed.
- The INCONCLUSIVE outcome and adversarial cases were tested in SDK direct mode; an INCONCLUSIVE live assessment is not claimed.
- No mobile-device/browser-matrix audit, mainnet deployment, video or social publication is claimed.

## Reproduce deployment

Use Studio to upload `contracts/museum_loan_iq.py` and deploy with no constructor arguments in Normal (Full Consensus) mode, using its built-in address. Alternatively run `node scripts/deploy.mjs`; it creates an ephemeral local development account by default, or uses `STUDIO_PRIVATE_KEY` when supplied securely for a dedicated test account. Do not use a key with real assets. Update `public/deployment.json` to the resulting contract before building.

`node scripts/live-smoke.mjs` is intended for a fresh deployment with unused `museum-demo-001`. It rejects duplicate IDs and does not overwrite existing evidence. Fixture URLs are pinned to the original fixture commit and hashes are computed from local bytes. `node scripts/collect-evidence.mjs` re-reads the existing final transactions and checks source equivalence without submitting writes.

For Python direct-mode setup, the test framework may try to download a release archive. If a release URL is unavailable but the official `genvm-lint` downloaded the same release archive, its identical cached archive can be reused in `~/.cache/gltest-direct/`. No SDK or tests were stubbed or modified to make them pass.
