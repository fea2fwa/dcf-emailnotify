import os
import smtplib
from dotenv import load_dotenv

def send_notification_email(sender_email, sender_password, recipient_emails, subject, body):
  """
  メールを送信する

  Args:
    sender_email: 送信元のメールアドレス
    sender_password: 送信元のメールアドレスのパスワード
    recipient_email: 受信者のメールアドレス
    subject: メールの件名
    body: メール本文
  """

  # print(f"出力確認ポイント1：{sender_email}, {sender_password}, {recipient_email}, {subject}, {body}")
  # ↑なぜかこのprint文を入れるとserver.sendmailでメール送信が出来なくなる！

  # SMTPサーバーに接続する
  server = smtplib.SMTP("mail67.conoha.ne.jp", 587)
  server.ehlo()
  server.starttls()
  server.login(sender_email, sender_password)

  new_sender_email = "notification@storage.dellcommunity.jp"
  print("新規コンテンツ情報：", body)

  main = "\n".join(body)

  print("main=", main)

  # メールを送信する
  message = "Subject: {}\n\n{}".format(subject, main)
  print("message情報：", message)

  for recipient_email in recipient_emails:
      server.sendmail(new_sender_email, recipient_email, message.encode('utf-8'))

  # SMTPサーバーを切断する
  server.quit()


if __name__ == "__main__":
  load_dotenv()  # .envファイルから環境変数を読み込む
  sender_email = os.environ.get("SENDER_EMAIL")
  sender_password = os.environ.get("SENDER_PASSWORD")
  # # 環境変数からメールアドレスとパスワードを取得する
  # sender_email = os.environ["SENDER_EMAIL"]
  # sender_password = os.environ["SENDER_PASSWORD"]
  last_texts = {1: "test", 2: "test2"}
  current_texts = {3: "tests", 4: "test4"}
  added = {k: v for k, v in current_texts.items() if k not in last_texts}

  body = []
  for i, v in added.items():
      body.append(f"タイトル：{i}, URL: https://www.dell.com/{v}")

  # メールを送信する
  try:
      recipient_emails = os.environ.get("TEST_RECIPIENT_EMAILS")
      recipient_emails = list(recipient_emails.split(","))
      print(recipient_emails)
      send_notification_email(
        sender_email, sender_password, recipient_emails, "Test email from uta", body
      )
  except Exception as e:
      print(f"メール送信に失敗しました：{e}")  

