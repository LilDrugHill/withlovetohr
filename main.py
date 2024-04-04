import requests
import smtplib
import dotenv

dotenv.load_dotenv()


def send_hello():
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(user=my_mail, password=password)
    s.sendmail(from_addr=my_mail, to_addrs='timur.shurak12@gmail.com', msg='hello')
    return print('Done')


if '__main__' == __name__:
    send_hello()
