# OPS Suite

OPS Suite is a Windows-friendly Django 5.2 application that centralises transition
and offboarding workflows while recording activity history. The full project now
lives inside the [`ops_suite/`](ops_suite/) directory.

## Where to work

```bash
cd ops_suite
```

Once inside that folder, follow the detailed documentation in
[`ops_suite/README.md`](ops_suite/README.md).

## Quick Start (summary)

1. Clone this repository **or** download `ops_suite/OPS_Suite.zip` and extract it.
2. From the repository root **or** within `ops_suite/`, run `INIT_WINDOWS.bat`
   (the script forwards to `ops_suite\scripts\INIT_WINDOWS.bat`) to prepare the
   virtual environment, install dependencies, apply migrations, collect static
   files, and ensure the default superuser exists.
3. Launch the development server with `START_DEV.bat` (available at the repository
   root, in `ops_suite\`, and under `ops_suite\scripts\`). Visit
   http://127.0.0.1:8000/ to explore the seeded dashboards.

For production, run `START_PROD.bat` (any location) to collect static files and
serve the site via Waitress on port 8080.

Refer to the ops_suite README for seed URLs, admin credentials, maintenance
scripts, troubleshooting tips, and GitHub publishing guidance.
