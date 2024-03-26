import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む
sender_account = os.environ.get("SENDER_EMAIL")
sender_password = os.environ.get("SENDER_PASSWORD")
recipient_emails = os.environ.get("TEST_RECIPIENT_EMAILS")

# 設定
smtp_server = 'mail67.conoha.ne.jp'
smtp_port = 587
smtp_username = sender_account
smtp_password = sender_password
sender_email = 'notification@storage.dellcommunity.jp'
receiver_email = recipient_emails

# メールを作成
subject = 'Dellコミュニティからのテストメール'
# message = "Hello World!"
body = 'テストメールの本文です。'
message = MIMEText(body, 'plain')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email

# SMTPサーバーに接続
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()
smtp_connection.login(smtp_username, smtp_password)

# メールを送信
smtp_connection.sendmail(sender_email, receiver_email, message.as_string())
# smtp_connection.sendmail(sender_email, receiver_email, message.encode('utf-8'))

# SMTPサーバーとの接続を閉じる
smtp_connection.quit()
