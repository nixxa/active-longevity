#coding: utf-8
""" Send email """

import logging
import re

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail

from application import app, config
from models import User

logger = logging.getLogger(__name__)

class MailProvider:
    """ Provider for sending e-mails """
    def __init__(self):
        self.api_key = config.SENDGRID_API_KEY
        self.email_pattern = ''
        return

    def send_registration_code(self, user: User):
        """
        Send notice
        """
        # check email
        code = user.confirm_code
        author_mail = user.email.lower()
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
            author_mail)
        if match is None:
            logger.error('E-mail adddress %s is wrong', author_mail)
            return
        sg_client = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email('noreply@%s' % config.HOSTNAME)
        to_email = Email(author_mail)
        subject = '[Московское долголетие] Код подтверждения'
        body = '<p>Код подтверждения: <strong>{code}</strong></p>\
            <p>Вы можете подтвердить email перейдя по \
            <a href="https://{host}/register/{user}/{code}/confirm/">ссылке</a> \
            '.format(host=config.HOSTNAME, code=code, user=user.guid)
        content = Content("text/html", body)
        mail = Mail(from_email, subject, to_email, content)
        mail_response = sg_client.client.mail.send.post(request_body=mail.get())
        if mail_response.status_code != 202:
            logger.error('Cant send email. Error is "%s"', mail_response.body)
        else:
            logger.info('E-mail sent')
        return

    def send_recover_link(self, user: User, action_id):
        """
        Send recover link
        """
        sg_client = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email('noreply@%s' % config.HOSTNAME)
        to_email = Email(user.email)
        subject = '[Московское долголетие] Восстановление пароля'
        body = '<p>Для восстановления пароля пройдите по ссылке: \
            <a href="https://{host}/recover/{code}/" target="_blank"> \
            https://{host}/recover/{code}/</a></p> \
            '.format(host=config.HOSTNAME, code=action_id)
        content = Content("text/html", body)
        mail = Mail(from_email, subject, to_email, content)
        mail_response = sg_client.client.mail.send.post(request_body=mail.get())
        if mail_response.status_code != 202:
            logger.error('Cant send email. Error is "%s"', mail_response.body)
        else:
            logger.info('E-mail sent')
        return
