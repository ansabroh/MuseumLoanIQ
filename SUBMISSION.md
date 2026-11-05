# Project submission

## Name
MuseumLoanIQ

## Short description
MuseumLoanIQ creates a shared, verifiable record for museum artifact loan disputes. Lenders register immutable handling and environmental terms; borrowers accept the exact terms hash. Parties commit version-pinned condition reports, transport records and logger evidence. A real GenLayer Intelligent Contract verifies evidence hashes, environmental limits and monitoring coverage, then uses independent validator review with source-grounded quotations to assess documented condition changes and transport compliance. The dashboard submits real transactions, waits for finalized successful execution, and displays append-only assessments and exportable receipts. Outcomes: COMPLIANT, REVIEW_REQUIRED, NONCOMPLIANT and INCONCLUSIVE. The live Studionet demonstration uses clearly labeled synthetic records. It does not claim physical inspection, artifact authentication, institutional identity verification or legal liability determination.

## Problem and trust mechanism
A lender and borrower can disagree about whether an artifact changed condition and whether handling met the agreement. A central chatbot can provide an answer without a shared commitment to inputs, reproducible checks, or independent review. MuseumLoanIQ fixes the loan terms and evidence bytes, enforces numeric checks deterministically, independently reviews ambiguous report language across GenLayer validators, and preserves each assessment in an auditable history.

## Reviewer walkthrough
1. Open the deployed dashboard and select `museum-demo-001`.
2. Inspect immutable terms and borrower acceptance.
3. Read its three recorded outcomes: COMPLIANT, REVIEW_REQUIRED and NONCOMPLIANT.
4. Expand full receipts and inspect exact quotes, evidence hashes and receipt links. Export the complete record.
5. Verify the deployed contract in the Studio explorer and compare its source against this repository.
6. For your own test, connect a Studio-style development signer, register a unique loan ID with a separate borrower address, accept as borrower, commit an authorized public packet and run assessment. README gives the exact schema and full process.

## Evidence

- Source: https://github.com/ansabroh/MuseumLoanIQ
- Contract: https://explorer-studio.genlayer.com/address/0xE6cc276002756C3F1123AD4Ce5d212eAf574D331
- Deployed source hash and byte comparison: `evidence/source-verification.json`.
- Ten finalized successful transactions: `evidence/verified-receipts.json`.
- On-chain assessment history: `evidence/live-loan.json`.
- Browser dashboard evidence: `evidence/dashboard.png`.
- Test and deployment details: `DEPLOYMENT.md`.

## Honest scope and next steps
The current application is a working Studionet prototype with synthetic demonstration documents. Its hosted dashboard initially uses owner-private access; reviewers need an owner-authorized public deployment or can run the complete source locally. No production launch, real institutional partnership, physical inspection, certification, video or public social post is claimed. A credible next stage is a registrar/conservator pilot using authenticated institutions, signed sensor exports and privacy-preserving report storage before production-network deployment.
