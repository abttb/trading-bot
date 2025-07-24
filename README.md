# 📈 trading-bot (IBKR Edition)

בוט מסחר אוטומטי המתחבר ל־Interactive Brokers (IBKR) דרך `ib_insync`, ומבצע קניות לפי רשימת מניות מוגדרת מראש.

## 🚀 איך זה עובד
- הבוט מתחבר ל־IB Gateway או TWS דרך API
- שולף נתוני שוק בזמן אמת
- מבצע פקודת BUY לפי ההגדרה
- רושם את כל הפעולות בקובץ לוג יומי

## 🛠️ קבצים חשובים
| קובץ | תיאור |
|------|--------|
| `bot.py` | הקובץ הראשי שמריץ את הבוט |
| `config.env` | משתני סביבה פרטיים (לא בריפו) |
| `config.env.example` | תבנית משתני סביבה |
| `utils/logger.py` | לוגים לקובץ ולמסך |
| `utils/trading.py` | חיבור, ניתוק, שליחת פקודות |
| `utils/config.py` | שליפת רשימת מניות מ־env |

## 📦 התקנה
```bash
git clone https://github.com/abttb/trading-bot.git
cd trading-bot
pip install -r requirements.txt
cp config.env.example config.env
# ערוך את config.env עם הפרטים שלך
