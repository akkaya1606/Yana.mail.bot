
import imaplib
import email
import time
import os

EMAIL = os.getenv("YANA_EMAIL")
PASSWORD = os.getenv("YANA_EMAIL_PASSWORD")
TARGET_SENDER = "akkayaridvan1606@gmail.com"

def check_mail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "UNSEEN")
        mail_ids = data[0].split()

        for i in mail_ids:
            result, msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = msg["From"]
            subject = msg["Subject"]
            if TARGET_SENDER in sender:
                print("Yeni mesaj var:")
                print("Konu:", subject)
                print("İçerik:")
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        print(part.get_payload(decode=True).decode())

    except Exception as e:
        print("Hata:", str(e))

if __name__ == "__main__":
    while True:
        check_mail()
        time.sleep(30)
