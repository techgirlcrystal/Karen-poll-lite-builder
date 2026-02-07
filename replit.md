# NIL Deals Poll App

## Overview
Interactive poll application asking "Should high school athletes be allowed to sign NIL deals?" with Yes/No/Not Sure options. Built for embedding in emails or websites.

## Tech Stack
- **Backend**: Python Flask (main.py)
- **Database**: replit.db for vote persistence
- **Frontend**: Single-page HTML with dark cinematic theme (templates/index.html)

## Project Structure
```
main.py              - Flask server with /vote and /results API endpoints
templates/
  index.html         - Dark-themed poll card UI
```

## How It Works
- Users see a dark card with three vote buttons
- On vote, buttons disappear and animated percentage bars appear
- Votes are persisted in replit.db across restarts
- API: POST /vote with {"choice": "yes"|"no"|"not_sure"}, GET /results

## Running
- Flask app runs on 0.0.0.0:5000
