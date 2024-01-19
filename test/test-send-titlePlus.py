import requests
from bs4 import BeautifulSoup
import time
import os
import smtplib
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import urllib.parse

def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # print(f"fetched dataは\n{soup}")

    # title = soup.title.string if soup.title else "No Title Found"
    # title = title.strip(" | DELL Technologies")
    # if "解決済み:" in title:
    #     title = title.strip("解決済み: ")

    # criptタグのtype "application/ld+json"からコンテンツを入手
    script_content = soup.find('script', {'type': 'application/ld+json'}).string

    # print(f"script_contentは{script_content}")

    # コンテンツをJSON形式でload、特殊文字が入っているのでstrict=Falseを設定
    json_data = json.loads(script_content, strict=False)

    print(f"json_dataは{json_data}")

    # JSONデータからmainEntityのtextを抜き出し
    question_text = json_data["mainEntity"]["text"]

    print(f"script_contentは{script_content}")

    author = json_data["mainEntity"]["author"]["name"]

    print(f"authorは{author}")

    post_time_gmt = json_data["mainEntity"]["datePublished"]

    print(f"post_time_gmtは{post_time_gmt}")

    post_time = convert_datetime_format(post_time_gmt)

    print(f"post_timeは{post_time}")

    return (author, post_time, question_text)


def convert_datetime_format(dt_str):
    # 文字列をPythonのdatetimeオブジェクトに変換
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # UTCからJSTに変換 (+9時間)
    dt_jst = dt + timedelta(hours=9)
    
    # 新しい形式に変換
    return dt_jst.strftime("%Y/%-m/%-d %-H:%M")


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
  current_texts = {"title1": "/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/data-domainextended-support-%E3%81%AE%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E5%86%85%E5%AE%B9%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/65a0ce9b4cc1fe3336e943ae",
                   "title2": "/community/ja/conversations/poweredgeサーバ/dell-power-edge-r660-電源冗長について/65a4fa767e38564e52a86bd5",
                   "title3": "/community/ja/conversations/ストレージ-コミュニティ/dm5500-24tbモデルの最大容量について/65a75311792ba45dca626b1d"}

  # current_texts = {"title1": "/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/data-domainextended-support-%E3%81%AE%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E5%86%85%E5%AE%B9%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/65a0ce9b4cc1fe3336e943ae",
  #                 }

  # current_texts = {"title2": "/community/ja/conversations/ストレージ-コミュニティ/powerscaleやネットワークスイッチのオートコールの連絡先変更について/65898f849222566d9dac5387"}

  added = {k: v for k, v in current_texts.items() if k not in last_texts}

  body = []
  for i, v in added.items():
    # v2 = f"https://www.dell.com/{v}"
    # v2 = "https://www.dell.com/"+str(v)
    url_utf8 = urllib.parse.quote(v, encoding="utf-8")
    v2 = f"https://www.dell.com{url_utf8}"
    print(f"確認URLは： {v2}")
    try:
        author, post_time, question_text = fetch_data_from_url(v2)
        if author is None:
            author = "（情報を取得できませんでした）"
        if post_time is None:
            post_time = "（情報を取得できませんでした）"
        if question_text is None:
            question_text = "（情報を取得できませんでした）"            
        print(f"コンテンツ内容＝タイトル：{i}, \n URL: {v2}, \n 質問者:{author}, \n Post time: {post_time}, \n 質問内容: \n {question_text} \n\n\n")
        # body.append(f"タイトル：{i}, \n URL: {v2}, \n 質問者:{author}, \n Post time: {post_time}, \n 質問内容: \n {question_text} \n\n\n")
        body.append(f"タイトル：{i}\nURL: {v2}\n質問者: {author}\nPost time: {post_time}\n質問内容:\n{question_text}\n\n\n")
    except Exception as e:
        print(f"コンテンツ詳細情報取得に失敗しました：{e}")  

      

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

