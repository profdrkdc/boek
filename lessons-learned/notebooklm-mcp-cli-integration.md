# Lesson Learned: Mandatory NotebookLM CLI Integration

## Context
The "Sovereign Reality" ecosystem relies on high-fidelity media generation (podcasts, reports, cinematic videos) via Google NotebookLM. Manual interaction is inefficient and prone to versioning errors.

## The Rule
Always use the `notebooklm-mcp-cli` (aliased as `nlm`) for:
1.  **Synchronization**: Ensuring the latest manuscript versions are uploaded as sources.
2.  **Generation**: Triggering the creation of targeted audio and video artifacts with specific focus topics.
3.  **Auditing**: Listing and evaluating studio artifacts to synchronize the `Asset-Evaluation.md` logbook.

## Implementation Details
- The CLI is installed in `/home/kareltestspecial/0-boek/00-GEREEDSCHAP/nlm_venv`.
- Due to potential path shifts, invoke the tool directly via its venv python:
  `/home/kareltestspecial/0-boek/00-GEREEDSCHAP/nlm_venv/bin/python3 -m notebooklm_tools.cli.main`
- This ensures the "Sovereign Reality" framework (Global v1.0) remains the single source of truth for all generated media.
