# TypeBattle – Interactive UI Edition

## What changed
- Beginner-first Practice flow: Warm-up Letters → Simple Words → Short Sentences → Full Keyboard.
- Live WPM, accuracy, errors, timer, progress bar and keyboard highlighting.
- Interactive Battle arena with difficulty, HP, combo, score and saved battle results.
- Login/Register use the same TypeBattle visual language as the main website.
- JWT authentication is used for saving practice/battle results.
- PostgreSQL-backed Leaderboard and Profile.

## Run
### Backend
From `backend`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Keep your existing `backend/.env` with your `DATABASE_URL`. Do not commit it.

### Frontend
From the project root:

```powershell
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`.
