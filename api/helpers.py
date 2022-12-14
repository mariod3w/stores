import random, re, os, string, base64, hashlib
from django.core.mail import EmailMultiAlternatives
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib import common
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

def randomword(length):
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(length))

def url_path(self, filename):
    name = randomword(12)
    filename, file_extension = os.path.splitext(filename)
    return "%s%s"%(name, re.sub('[^A-Za-z0-9.]+', '', file_extension))

def send_email(asunto, receptor, html, sender=os.getenv("SENDER"), sender_email=os.getenv("SENDER_EMAIL")):
    email = EmailMultiAlternatives(
        subject=asunto,
        body=html,
        from_email="%s <%s>"%(sender, sender_email),
        to=[receptor],
        reply_to=["%s"%sender_email]
    )
    email.attach_alternative(html, 'text/html')
    email.send()

def generate_token(user): 
    application = Application.objects.get(client_id=os.getenv("OAUTH_CLIENT_ID"))
    expires = datetime.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    print(application, expires)
    access_token = AccessToken(
        user=user,
        scope='read write',
        expires=expires,
        token=common.generate_token(),
        application=application
    )
    access_token.save()
    return access_token