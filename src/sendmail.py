""" Send email """
import logging
import os
import re

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail

logger = logging.getLogger(__name__)

class MailProvider:
    """ Provider for sending e-mails """
    customer_email = os.environ.get('CUSTOMER_EMAIL', '')
    manager_email = os.environ.get('MANAGER_EMAIL', '')

    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        self.email_pattern = ''
        return

    def send_checklist_notice(self, author_mail, checklist):
        """
        Send notice
        :type author_mail: str
        :type checklist: model.Checklist
        """
        # check email
        author_mail = author_mail.lower()
        match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                         author_mail)
        if match is None:
            logger.error('E-mail adddress %s is wrong', author_mail)
            return
        sg_client = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email('noreply@secret-shopper.net')
        to_email = Email(author_mail)
        subject = "[SecretShopper] АЗС #{0}".format(checklist.object_info.num)
        body = "<h2>Контрольный лист посещения сохранен</h2>\
            <p>Для исправления анкеты необходимо перейти по ссылке \
            <a href='https://secret-shopper.net/checklist/edit/{0}'>https://secret-shopper.net/checklist/edit/{0}</a></p>\
            <p>Для добавления файлов воспользуйтесь ссылкой \
            <a href='https://secret-shopper.net/checklist/addfiles/{0}'>https://secret-shopper.net/checklist/addfiles/{0}</a></p>\
            <p><br/><br/><br/><br/><br/><hr /><small>Это сообщение сформировано автоматически, на него не нужно отвечать.</small>\
            </p>".format(checklist.uid)
        content = Content("text/html", body)
        mail = Mail(from_email, subject, to_email, content)
        if MailProvider.manager_email != '':
            logger.debug('CC: %s', MailProvider.manager_email)
            mail.personalizations[0].add_cc(Email(MailProvider.manager_email))
        mail_response = sg_client.client.mail.send.post(request_body=mail.get())
        if mail_response.status_code != 202:
            logger.error('Cant send email. Error is "%s"', mail_response.body)
        else:
            logger.info('E-mail sent')
        return


    def send_checklist_verified(self, checklist):
        """
        Send e-mail to authorities
        """
        if MailProvider.customer_email == '':
            return
        sg_client = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email('noreply@secret-shopper.net')
        to_email = Email(MailProvider.customer_email)
        subject = "[SecretShopper] АЗС #{0} добавлена".format(checklist.object_info.num)
        body = "<h2>Контрольный лист посещения добавлен</h2>\
            <p>Для просмотра анкеты необходимо перейти по ссылке \
            <a href='https://secret-shopper.net/checklist/edit/{0}'>https://secret-shopper.net/checklist/edit/{0}</a></p>\
            <p><br/><br/><br/><br/><br/><hr /><small>Это сообщение сформировано автоматически, на него не нужно отвечать.</small>\
            </p>".format(checklist.uid)
        content = Content("text/html", body)
        mail = Mail(from_email, subject, to_email, content)
        mail_response = sg_client.client.mail.send.post(request_body=mail.get())
        if mail_response.status_code != 202:
            logger.error('Cant send email. Error is "%s"', mail_response.body)
        return
