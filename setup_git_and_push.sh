
#!/bin/bash
set -e
if [ ! -d trading-bot ]; then
  echo "📦 יצירת תיקיית הבוט"
  mkdir trading-bot
fi
cd trading-bot || exit
if [ ! -d .git ]; then
  echo "🔧 אתחול Git"
  git init
fi
if ! git remote get-url origin > /dev/null 2>&1; then
  echo "🔗 חבר את ה-Repo שלך ב-GitHub"
  read -p "הזן את כתובת ה-URL של ה-Repo שלך ב-GitHub: " repo_url
  git remote add origin "$repo_url"
fi
echo "➕ הוספת כל הקבצים והכנת Commit"
git add .
git commit -m "Initial commit of complete trading bot package" || echo "🔹 אין שינויים להוסיף לקומיט"
git branch -M main
echo "🚀 דחיפת הקוד ל-GitHub"
git push -u origin main
echo "✅ העלאה הושלמה. הקוד שלך זמין ב-GitHub."
