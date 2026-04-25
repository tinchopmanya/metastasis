# Scripts

This folder will hold lightweight validation scripts for CRLM.

Initial direction:

1. Read `data_manifest/signatures.yml`.
2. Fetch or document metadata for GEO sources.
3. Prepare first-pass gene set scoring.
4. Keep image downloads out of scope until the molecular hypothesis is prioritized.

Preferred first script:

`prepare_signatures.py`

Expected output:

- normalized signature table
- missing gene report per dataset
- markdown summary for the next research log
