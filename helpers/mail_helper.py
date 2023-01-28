"""Module contains implementation of sending emails and probably
should be deprecated"""
import os
import os.path
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from helpers import converters


class Mail:
    """Class contains implementation of sending emails"""
    def __init__(self, body, from_addr, to_addr, mypass, subject, files, logger):
        self.body = body
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.mypass = mypass
        self.subject = subject
        self.files = files
        self.logger = logger

    def generate_mail_text(self, comparing_info, sql_comparing_properties, data_comparing_time, schema_comparing_time)\
            -> None:
        """Method generates email text"""
        text = "Initial conditions:\n\n"
        if sql_comparing_properties.get('check_schema'):
            text = text + "1. Schema checking enabled.\n"
        else:
            text = text + "1. Schema checking disabled.\n"
        if sql_comparing_properties.get('fail_with_first_error'):
            text = text + "2. Failed with first founded error.\n"
        else:
            text = text + "2. Find all errors\n"
            text = text + "3. Report checkType is " + sql_comparing_properties.get('mode') + "\n\n"
        if any([comparing_info.empty, comparing_info.diff_data, comparing_info.no_crossed_tables,
                comparing_info.prod_uniq_tables, comparing_info.test_uniq_tables]):
            text = self.get_test_result_text(comparing_info)
        else:
            text = text + "It is impossible! There is no any problems founded!"
        if sql_comparing_properties.get('check_schema'):
            text = text + "Schema checked in " + str(schema_comparing_time) + "\n"
        text = text + "Dbs checked in " + str(data_comparing_time) + "\n"
        return text

    def sendmail(self) -> None:
        """Method sends email"""
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        if isinstance(self.to_addr, list):
            msg['To'] = ', '.join(self.to_addr)
        else:
            msg['To'] = self.to_addr
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'plain'))
        if self.files is not None:
            for attach_file in self.files.split(','):
                if os.path.exists(attach_file) and os.path.isfile(attach_file):
                    with open(attach_file, 'rb') as file:
                        part = MIMEApplication(file.read(), Name=basename(attach_file))
                    part['Content-Disposition'] = f'attachment; filename="{basename(attach_file)}"'
                    msg.attach(part)
                else:
                    if attach_file.lstrip() != "":
                        self.logger.error(f"File not found {attach_file}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        try:
            server.login(self.from_addr, self.mypass)
            text = msg.as_string()
            server.sendmail(self.from_addr, self.to_addr, text)
            server.quit()
        except smtplib.SMTPAuthenticationError:
            self.logger.error('Raised authentication error!')

    def get_test_result_text(self, comparing_info) -> str:
        """Method prepare body of email"""
        body = self.body + "There are some problems found during checking.\n\n"
        if comparing_info.empty:
            body = body + "Tables, empty in both dbs:\n" + ",".join(comparing_info.empty) + "\n\n"
        if comparing_info.prod_empty:
            body = body + "Tables, empty on production db:\n" + ",".join(comparing_info.prod_empty) + "\n\n"
        if comparing_info.test_empty:
            body = body + "Tables, empty on test db:\n" + ",".join(comparing_info.test_empty) + "\n\n"
        if comparing_info.diff_data:
            body = body + "Tables, which have any difference:\n" + ",".join(comparing_info.diff_data) + "\n\n"
        if list(set(comparing_info.empty).difference(set(comparing_info.no_crossed_tables))):
            body = body + "Report tables, which have no crossing dates:\n" + ",".join(
                list(set(comparing_info.empty).difference(set(comparing_info.no_crossed_tables)))) + "\n\n"
        if comparing_info.get_uniq_tables("prod"):
            body = body + "Tables, which unique for production db:\n" + ",".join(
                converters.convert_to_list(comparing_info.prod_uniq_tables)) + "\n\n"
        if comparing_info.get_uniq_tables("test"):
            body = body + "Tables, which unique for test db:\n" + ",".join(
                converters.convert_to_list(comparing_info.test_uniq_tables)) + "\n\n"
        return body
