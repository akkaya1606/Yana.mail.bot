import imaplib
import email
import time
import os
import smtplib
from email.mime.text import MIMEText

# Ortam değişkenlerinden e-posta adresi ve şifre alınır
EMAIL = os.getenv("YANA_EMAIL")
PASSWORD = os.getenv("YANA_EMAIL_PASSWORD")
TARGET_SENDER = "akkayaridvan1606@gmail.com"

# Yanıt gönderme fonksiyonu
def send_response(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = TARGET_SENDER

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [TARGET_SENDER], msg.as_string())
        server.quit()
        print("Yanıt e-postası gönderildi.")
    except Exception as e:
        print("Yanıt gönderme hatası:", str(e))

# Mail kontrol fonksiyonu
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

            sender = msg.get("From", "(Unknown Sender)")
            subject = msg.get("Subject", "(No Subject)")

            if not isinstance(sender, str):
                sender = str(sender)
            if not isinstance(subject, str):
                subject = str(subject)

            print("Yeni mesaj var:")
            print("Gönderen:", sender)
            print("Konu:", subject)

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True).decode(errors='replace')
                    print("İçerik:\n", content)
                    send_response("YANA'dan Yanıt", f"Mesajını aldım: {content}")
    except Exception as e:
        print("Hata:", str(e))

# Sürekli dinleme döngüsü
if __name__ == "__main__":
    while True:
        check_mail()
        time.sleep(30)
