# MuseumLoanIQ

MuseumLoanIQ gives lenders and borrowers a shared, tamper-evident record of whether museum artifact handling is supported by their loan documentation. The dashboard calls a real GenLayer Intelligent Contract; its outcomes are COMPLIANT, REVIEW_REQUIRED, NONCOMPLIANT and INCONCLUSIVE.

## What is different

Loan disputes involve two separate questions: did measured environmental conditions breach the agreement, and do narrative condition/transport reports support compliance? Integer checks settle the first. Independently executed validator reviews settle the documented interpretation, with exact quotation checks and agreement on both condition and transport classifications. A new condition change requires human review; it does not prove fault.

## Run

Requires Node 22+ and Python 3.12+.

```sh
npm ci
npm run dev
npm test
pip install -r requirements-dev.txt
python -m pytest tests/test_contract.py -q
genvm-lint check contracts/museum_loan_iq.py
npm run build
```

`public/deployment.json` identifies the deployed Studionet contract (chain 61999). The built-in Studio address used for the final deployment is recorded in `evidence/studio-deployment-receipt.json`. Deployment source was byte-for-byte checked with `getContractCode`.

## Use the dashboard

1. Open the loan workspace. Read the seeded `museum-demo-001` without connecting an account. This is explicitly synthetic data, not a real museum loan.
2. Select **Use Studio account**. Create a local development account, using the same `createAccount` signing method as Studio. MetaMask is unnecessary. A dedicated development key can be imported for repeat access; the app keeps it only in page memory. Copy the public connected address from transaction activity before sharing it with a lender. Reloading clears the signer; retain your dedicated development key independently if you need continued ownership.
3. As lender, register a unique ID and JSON loan terms. The `borrower` must be a different address. The lender's transaction sender, rather than the institution-name string, controls the record. Terms cannot be edited.
4. As borrower, connect the matching account and accept the exact terms hash. Acceptance is required for COMPLIANT.
5. Prepare a public evidence JSON packet using `evidence/sample-packet.json`. Replace all synthetic data with authorized institution reports and actual logger exports. Include issuer names and document references. Do not upload confidential condition reports to public GitHub.
6. Commit the packet to GitHub. Use its raw URL containing the full 40-character commit SHA, and SHA-256 of the exact UTF-8 file bytes (`sha256sum packet.json`). Submit the URL, hash and explanatory note.
7. Run assessment as either loan party. The dashboard shows the transaction hash, pending consensus stages, final execution status, then refreshes the on-chain record. Use Resume tracking after a network interruption. It never automatically resubmits a pending write.
8. Inspect and export the full record. Up to three distinct evidence versions are supported; earlier assessments and their hash chain remain unchanged. Submit a new packet and challenge note to request another assessment.

## Evidence schema

`loan_id` and `artifact_id` must match the immutable registration. `before_report`, `after_report`, and `transport_report` are attributed text (12–6000 characters each); `sources` contains 1–8 `{issuer,reference}` objects. `readings` contains 2–512 strictly chronological records with `time`, `temp_c100` and `rh_pct100` integers. Temperature is °C ×100; humidity is %RH ×100; time is Unix seconds. Monitoring must start/end exactly at the agreed boundaries, with no gaps exceeding `max_gap_seconds`, to support COMPLIANT. Boundary values are inclusive.

Pinned evidence is fetched by the contract, checked against its declared SHA-256 and 40 KB limit, and agreed through strict equality. URLs are restricted to commit-pinned raw.githubusercontent.com JSON paths. This restriction limits retrieval scope; it does not certify the publisher's authority. Retrieval/hash/schema failures revert and leave evidence pending for an explicit retry. Invalid committed evidence cannot be replaced in-place: a fresh loan ID is required if a pending packet is permanently invalid. Choose and validate packets carefully.

## Outcome rules

| Outcome | Rule |
|---|---|
| NONCOMPLIANT | At least one documented numeric breach, or complete coverage plus consensus-confirmed transport violation |
| REVIEW_REQUIRED | Complete environmental coverage, no numeric breach, satisfied transport, and a documented condition change |
| INCONCLUSIVE | Missing coverage, uncertain/invalid semantic review, or otherwise-compliant evidence without borrower acceptance |
| COMPLIANT | Complete coverage, no breach, borrower acceptance, unchanged documented condition and satisfied transport |

Numeric breaches take priority even when coverage is incomplete. Insufficient coverage bypasses semantic review and remains INCONCLUSIVE. Three exact, source-specific quotations are mandatory for semantic results. The validator independently reruns the review before comparing its two classification fields with the leader's; reasoning text need not match byte-for-byte. Consensus failure can leave a transaction undetermined rather than create an assessment receipt. The UI treats this as failure.

## Architecture

- `contracts/museum_loan_iq.py`: standalone contract, authorization, evidence retrieval, deterministic checks, independent semantic consensus and hash-linked receipts.
- `src/main.js`: real SDK read/write calls, Studio-style development signing and dashboard.
- `src/lifecycle.js`: finality/execution checks, bounded polling and resumable transaction handling.
- `tests/`: SDK direct-mode contract tests and frontend lifecycle tests.
- `evidence/`: clearly labeled synthetic packets and live validation records.
- `DEPLOYMENT.md`, `SECURITY.md`, `SUBMISSION.md`: deployment, boundaries and reviewer notes.

## Trust boundaries and future use

The authoritative inputs for a real case are the parties' accepted loan terms, their original institution condition/transport reports and their logger records. No generic preservation threshold is substituted for the actual loan agreement. The demonstration does not claim these synthetic documents are authoritative. Source attribution and hashing establish what was assessed, not whether an institution or sensor was truthful. Wallet control does not certify museum identity. This is a documentary assessment, not physical inspection, artifact authentication, regulatory certification, legal judgment, or proof of causation.

Studionet is a development network and may reset. No mainnet/Bradbury deployment, production audit, institutional pilot, real museum adoption, or media publication is claimed. Continued use would require institution identity verification, signed logger exports, confidential evidence handling, production network deployment, and a pilot with registrars and conservators.

## Official references

- https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism
- https://docs.genlayer.com/developers/intelligent-contracts/testing
- https://docs.genlayer.com/api-references/genlayer-js
- https://github.com/genlayerlabs/genlayer-studio/blob/main/frontend/src/hooks/useGenlayer.ts

MIT licensed. The dashboard's vessel is a purpose-built SVG illustration, not a photograph of an authenticated object.
