# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python CLI tool that scrapes data usage from Iliad Italy accounts (iliad.it). Logs into the account page, extracts the data progress percentage, and calculates GB used based on the user's plan.

## Commands

```bash
# Install dependencies
poetry install

# Run the scraper (default make target)
make

# Format and lint code (isort → black → flake8)
make fmt

# Run with debug output
DEBUG=1 make
```

## Architecture

Single-module package in `iliad_account/__init__.py`:
- `main()` - CLI entry point, loads .env, orchestrates login and scraping
- `login()` - Authenticates via POST to iliad.it/account/
- `get_progress_value()` - Parses HTML for `data-progress-value` attribute
- `get_credentials()` - Reads from env vars or prompts interactively

Entry point registered in `[project.scripts]` as `iliad_account`.

## Configuration

Credentials via `.env` file (see `.env.example`):
- `ILIAD_USER_ID` - 8-digit user ID
- `ILIAD_PASSWORD` - Account password
- `ILIAD_DATA_GB` - Total GB in plan (for calculating usage)
- `DEBUG` - Set to `1` for verbose output
