import os
import smtplib
from dotenv import load_dotenv

def send_notification_email(sender_email, sender_password, recipient_email, subject, body):
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

  body = {"hello":"world"}
  new_sender_email = "notification@storage.dellcommunity.jp"

  # メールを送信する
  message = "Subject: {}\n\n{}".format(subject, body)
  server.sendmail(new_sender_email, recipient_email, message)

  # SMTPサーバーを切断する
  server.quit()


if __name__ == "__main__":
  load_dotenv()  # .envファイルから環境変数を読み込む
  sender_email = os.environ.get("SENDER_EMAIL")
  sender_password = os.environ.get("SENDER_PASSWORD")
  # # 環境変数からメールアドレスとパスワードを取得する
  # sender_email = os.environ["SENDER_EMAIL"]
  # sender_password = os.environ["SENDER_PASSWORD"]

  # メールを送信する
  try:
      send_notification_email(
        sender_email, sender_password, "yutaro.uehara@dell.com", "Test email from uta", "This is a test email."
      )
  except Exception as e:
      print(f"メール送信に失敗しました：{e}")  

