# Security and assessment boundaries

This is a development-network documentary assessment. No production audit is claimed.

## Enforced properties

- The registering sender owns the lender role. Borrower is immutable and must be a different address. Only these two addresses can submit or assess; only borrower can accept the exact terms hash.
- Loan terms are immutable. Evidence versions and assessments are append-only, limited to three. Each receipt includes the prior receipt hash (or original terms hash), evidence hash, terms hash, assessor and acceptance snapshot.
- Evidence URLs allow only HTTPS raw.githubusercontent.com paths with an explicit 40-character lowercase commit SHA and JSON suffix. No arbitrary domains, credentials, query strings or traversal paths are accepted. Contract does not perform secondary retrieval of cited source references.
- The response must be HTTP 200, no more than 40,000 bytes and match the declared SHA-256. The cap is checked after retrieval; the host/network controls actual download limits. There is no claim of a pre-download streaming cap or custom redirect enforcement.
- Identity, source attribution, reading units/ranges, chronological order, complete period coverage and inclusive numeric limits are validated before semantic review. Missing coverage cannot pass. A breach cannot be overruled by an LLM.
- The semantic prompt treats supplied terms and reports as untrusted data. Each independent reviewer must produce three verbatim report-specific quotations. The validator reruns the task independently and compares condition/transport classifications rather than rubber-stamping the leader or checking only JSON shape.
- Signature/consensus/transaction failure is separate from an application assessment. Only finalized successful execution is shown as complete. Pending transaction hashes are retained for explicit resumption; no automatic duplicate submission.
- Keys are local development signers created by the SDK or imported by the visitor. They stay in page memory, are never uploaded, logged, or saved by this app, and clear on reload. The imported key field is cleared after use. Account creation is intended for disposable exploration; ongoing ownership requires an independently retained dedicated development key.

## Not established

Hashes establish byte identity, not factual truth, sensor calibration, museum identity or source authenticity. Attribution is self-attested. Before using real documents, parties must verify issuer identity and use authorized institution records and signed logger exports. Both parties accepting the terms does not authenticate subsequent evidence. The contract cannot inspect physical damage or infer liability. Quotation grounding does not guarantee that an LLM interpreted quoted content correctly; independent consensus mitigates rather than eliminates this risk.

An invalid pending packet blocks subsequent submissions for that loan. Transient retrieval errors can be retried; permanently invalid packets require a new loan ID. The three-version limit is an explicit resource bound, not a full dispute tribunal. No time-based challenge deadline is claimed.

## Production prerequisites

Independent audit, authenticated institutions, signed evidence provenance, encrypted/confidential evidence architecture, robust hosted wallet/identity UX, production fee profiles and persistent-network deployment. The published demo contains no real institution records. The publicly known test keys in the live-smoke script are disposable fixtures, not operational credentials and must never receive funds.

Report a reproducible issue through the repository's GitHub Issues without posting confidential documents or wallet secrets.
