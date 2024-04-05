import requests
import smtplib
import dotenv
import bs4
import os
import re
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


dotenv.load_dotenv()
PASSWORD = os.getenv('PASSWORD')
MY_MAIL = os.getenv('MY_MAIL')
STMP_SERVER = os.getenv('STMP_SERVER')
WEB = os.getenv('POLSKA_WEBSITE')
RESUME_PATH = os.getenv('RESUME_PATH')
MASSAGE_PATH = os.getenv('MASSAGE_PATH')


def main():
    send_massages(get_hr_boxes_with_company_names(requests.get(WEB)))


def get_hr_boxes_with_company_names(request):
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    data_set = []
    for unit in soup.find_all(name='details'):
        company_data = (unit.summary.text.replace('\xa0', ' '),
                        *re.findall(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                                    string=unit.text))

        data_set.append(company_data) if len(company_data) == 2 else None
    return data_set


def send_massages(do_they_hate_me_list):
    server = smtplib.SMTP(host=STMP_SERVER, port=587)
    server.starttls()
    server.login(user=MY_MAIL, password=PASSWORD)
    for company_data in do_they_hate_me_list:
        try:
            server.send_message(from_addr=MY_MAIL,
                                to_addrs=company_data[1],
                                msg=prepare_message(company_data[0]))
        except BaseException as ex:
            print(ex)

    return print('Done')


def prepare_message(company):
    msg = MIMEMultipart()
    msg['Subject'] = 'Resume'
    filename = os.path.basename(RESUME_PATH)
    ctype, encoding = mimetypes.guess_type(RESUME_PATH)
    maintype, subtype = ctype.split('/', 1)

    with open(RESUME_PATH, 'rb') as fp:
        file = MIMEBase(maintype, subtype)
        file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)

    with open(MASSAGE_PATH, "r") as f:
        msg.attach(MIMEText(f.read().format(company=company), 'plain'))

    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)
    return msg


if '__main__' == __name__:
    main()
