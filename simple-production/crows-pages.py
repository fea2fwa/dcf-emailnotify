import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
import smtplib

def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # すべての<a>タグを検索
    links = soup.find_all('a', title=True, href=True)

    # 各リンクのtitleとhrefをディクショナリに保存
    title_url_dict = {link['title']: link['href'] for link in links}

    return(title_url_dict)
    

def send_notification_email(sender_email, sender_password, recipient_emails, subject, body):
    # SMTPサーバーに接続する
    server = smtplib.SMTP("mail67.conoha.ne.jp", 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email, sender_password)

    # リスト内に複数情報がある場合には複数行に分けて記載する
    main = "\n".join(body)

    # メールを送信する
    message = "Subject: {}\n\n{}".format(subject, main)
    print(f"メッセージは：{message}")

    # 実際にユーザーから見える送信元メールアドレス
    new_sender_email = "notification@storage.dellcommunity.jp"

    print(f"出力確認ポイント2：email送信開始")

    # メール送信部分　.encode('utf-8')は'ascii' codec can't encode characters in position 13-34: ordinal not in range(128)エラー対策
    for recipient_email in recipient_emails:
        server.sendmail(new_sender_email, recipient_email, message.encode('utf-8'))

    print(f"出力確認ポイント3：email送信完了")

    # SMTPサーバーを切断する
    server.quit()

def check_for_updates(url, check_interval=300):
    print("Starting to monitor websites for updates...")

    last_texts = fetch_data_from_url(url)

    print(last_texts)

    while True:
        time.sleep(check_interval)

        current_texts = fetch_data_from_url(url)
        if current_texts is None:
            continue

        if current_texts != last_texts:
            print(f"Update detected on {url}!")
            added = {k: v for k, v in current_texts.items() if k not in last_texts}
            print("新規コンテンツ情報：", added)

            body = []
            for i, v in added.items():
                body.append(f'タイトル：{i}, URL: "https://www.dell.com{v}"')

            # 環境変数からメールアドレスとパスワードを取得する
            load_dotenv()  # .envファイルから環境変数を読み込む
            sender_email = os.environ.get("SENDER_EMAIL")
            sender_password = os.environ.get("SENDER_PASSWORD")

            # メールを送信する
            try:
                recipient_emails = os.environ.get("RECIPIENT_EMAILS")
                recipient_emails = list(recipient_emails.split(","))
                send_notification_email(
                  sender_email, sender_password, recipient_emails, "Dellコミュニティに新規コンテンツが投稿されました", body
                )
            except Exception as e:
                print(f"メール送信に失敗しました：{e}")

            print(f"出力確認ポイント4：email送信処理に投げたことを確認")

            # 最新のコンテンツを今後の比較対象とする
            last_texts = current_texts



def main():
    url_to_check = "https://www.dell.com/community/ja/categories/%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%EF%BC%86%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9"

    try:
        check_for_updates(url_to_check)
    except Exception as e:
        print(f"アップデート確認処理に失敗しました：{e}")


if __name__ == "__main__":
    main()




