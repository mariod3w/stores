import os
from celery import shared_task
from django.core.mail import send_mail 
from django.contrib.auth.models import User 
from stores_backend.settings import base
from .models import StoreSuscription
from .helpers import send_email

@shared_task
def send_emails_suscribers():
	for suscription in StoreSuscription.objects.all():
		user = suscription.user
		store = suscription.store
		asunto = 'Nueva oferta en %s'% store.name
		mensaje = 'Hola %s <br> Te informamos que %s ha publicado una nueva oferta en su tienda. <br> <a href="https://sportline.com.hn">Ver oferta</a>'%(user.name, store.name)
		send_email(asunto, user.email, mensaje, store.name, "contacto@infolucion.com")
