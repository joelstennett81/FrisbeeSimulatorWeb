# 🥏 Frisbee Simulator

A Django web app that simulates Ultimate Frisbee games, calculates player skill ratings from UFA stats, and displays detailed game and player insights.

---

## 🚀 Features

- ✅ Simulate UFA games
- ✅ View point-by-point breakdowns with interactive links
- ✅ Calculate player skill ratings based on season stats
- ✅ Normalize scores using a curved distribution
- ✅ Adjust skill ratings lightly based on team success (wins)
- ✅ Dynamic Bootstrap UI with stat leaderboards
- ✅ User authentication & profile management

---

## 📊 Skill Rating System

The app uses a custom skill map to assign players a 1–100 score for each category. Skills are computed by:

1. **Summing stat fields per skill**
2. **Applying minor penalties for negative actions (e.g. drops, throwaways)**
3. **Lightly weighting team wins**
4. **Normalizing all scores with a curved distribution**
5. **Saving per-skill scores + overall role-based ratings**

Example skill mapping:
```python
"handle_cut_offense": ["catches", "drops"],
"deep_huck_throw_offense": ["hucks_completed", "yards_thrown", "throwaways", "assists", "pulls"],
```

---

## 🛠️ Tech Stack

- **Backend:** Django + PostgreSQL
- **Frontend:** Bootstrap 4, jQuery, Select2
- **Data:** Custom models for UFAPlayer, UFAPlayerStatsYear, Game, Point, Team
- **Normalization:** NumPy for stat curves

---

## 📫 Contact

Maintained by [Joel Stennett](mailto:joelstennett17@gmail.com)
