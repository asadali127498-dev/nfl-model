# Project context for Claude Code

This is an NFL prediction model (Elo-based, Python + `nfl_data_py`).

## Planning notes live in Google Drive (private)

The project plan and running progress log are intentionally kept **out of this
public repo**. They live in the owner's Google Drive as two files:

- **PROJECT.md** — what the project is, goals, stack.
- **PROGRESS.md** — what's done, known issues, and next steps.

**At the start of a session, if the Google Drive connector is available:**
search Drive for the files titled `PROJECT.md` and `PROGRESS.md`, read them, and
treat them as authoritative context for the project's goals and current state.
If the connector is not available, continue using the code and this file alone,
and let the user know the Drive notes couldn't be loaded.

**At the end of a working session**, offer to update `PROGRESS.md` in Drive with
what changed and the new next steps.

> Note: this auto-load only works in sessions that have the Google Drive
> connector enabled (e.g. Claude Code on the web). A plain local CLI without the
> connector won't be able to reach the Drive notes.
