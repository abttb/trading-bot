
import logging
from datetime import datetime
from ib_insync import IB, Stock

# הגדר מיקום קובץ הלוג שלך
log_file_path = '/root/trading-bot/bot.log'
output_file_path = '/root/trading-bot/diagnostics_output.txt'

def check_trading_activity(log_path):
    try:
        with open(log_path, 'r') as log:
            content = log.read()
            if 'submitOrder' in content or 'Placed order' in content:
                return '✅ נמצאו פקודות קנייה או מכירה בלוג'
            elif 'שוק סגור' in content:
                return 'ℹ️ השוק היה סגור - לא נשלחו פקודות'
            elif 'No symbols matched' in content:
                return '❌ לא נמצאו מניות שעונות על התנאים'
            elif 'API connection failed' in content:
                return '❌ חיבור API נכשל'
            else:
                return '⚠️ לא נמצאה פעילות מסחר בלוג. ייתכן שהבוט רץ אך לא שלח פקודות.'
    except FileNotFoundError:
        return '❌ קובץ לוג לא נמצא'

def main():
    status = check_trading_activity(log_file_path)
    with open(output_file_path, 'w') as out:
        out.write(f'{datetime.now()}: {status}\n')
    print(status)

if __name__ == '__main__':
    main()
