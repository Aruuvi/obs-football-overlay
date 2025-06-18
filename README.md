# OBS Single Match Timer & Scoreboard

A simple OBS Studio script written in Python for managing the score and timer of a single match between two teams. Ideal for small sports events, streams, or esports where a clean, manual scoreboard and timer are needed.

---

## 🧰 Features

- Displays score for **2 teams**.
- Displays a **custom match timer** (default: 12 minutes).
- Timer automatically stops when the match duration is reached.
- Buttons for increasing/decreasing team scores.
- Buttons for starting/stopping/resetting the timer.
- Works with any **text source** in OBS.

---

## 🖥️ How to Use

1. **Download or clone** this repository.
2. Open OBS Studio.
3. Go to `Tools` > `Scripts`.
4. Click the ➕ button to add a new script and select `obs-football-overlay.py`.
5. Set the following in the right panel:
   - Select a **text source** for `Team 1`, `Team 2`, and the `Timer`.
   - Set the **Match Duration (minutes)**.
6. Use the buttons to update scores or control the timer.
7. The timer will stop automatically when time is up.

---

## 🛠 Requirements

- OBS Studio (tested with version ≥ 28)
- Python 3.11
- OBS text sources (`GDI+`, `FT2`, or `Text v2`)

---

## 👤 Author

Created by Aruuvi. Contributions and forks welcome!
