import sys
import imaplib
import email
import os

server = "imap.yandex.ru"
login = "mail"
password = "pass"
putdir = "./home/"

"""- подключаемся к imap.yandex.ru -"""
mail = imaplib.IMAP4_SSL(server)

""" логинимся"""
mail.login(login, password)
mail.list()

""" подключаемся к inbox (входящие)"""
mail.select("inbox")

""" получаем UID последнего письма"""
result, data = mail.uid('search', None, "ALL")

for num in data[0].split():
    result, data = mail.fetch(num, '(RFC822)')
    print(mail.fetch(num, '(RFC822)'))
    raw_email = data[0][1]
    try:
        email_message = email.message_from_string(raw_email)
    except TypeError:
        email_message = email.message_from_bytes(raw_email)
    for part in email_message.walk():
        if "application" in part.get_content_type():
            filename = part.get_filename()
            filename = str(email.header.make_header(email.header.decode_header(filename)))
            print(filename)
            if not (filename): filename = "test.csv"
            fp = open(os.path.join(putdir, filename), 'wb')
            fp.write(part.get_payload(decode=1))
            fp.close
    """ удаляем письмо из почты"""
    mail.store(num, '+FLAGS', '(\Deleted)')
    mail.expunge()
mail.close()
mail.logout()
