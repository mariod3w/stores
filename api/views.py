from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from .helpers import randomword, send_email, generate_token
from django.contrib.auth import authenticate, login, logout


from .serializers import *

class AbstractViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        # account = get_account(self.request.user)
        # branch = get_branch(self.request.user)
        if self.request.user.is_authenticated:
            serializer.save(
                created_user=self.request.user, 
                # active=True, 
                # status=get_status_enable(),
                # account=account,
                # branch=branch
            )
        else: 
            serializer.save()

            # if account:
            #     obj.accounts.add(account)
            # if branch:
            #     obj.branches.add(branch)
    
    def perform_update(self, serializer):
        serializer.save(updated_user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted = datetime.now()
        obj.deleted_user = request.user
        obj.save()
        return Response(data='delete success')

class BrandViewSet(AbstractViewSet):
    queryset = Brand.objects.filter(deleted__isnull=True)
    serializer_class = BrandSerializer

class StoreViewSet(AbstractViewSet):
    queryset = Store.objects.filter(deleted__isnull=True)
    serializer_class = StoreSerializer

class DealViewSet(AbstractViewSet):
    queryset = Deal.objects.filter(deleted__isnull=True)
    serializer_class = DealSerializer

class AuthView(APIView): 
    def post(self, request, format=None):
        user = MyUser.objects.filter(email=request.data['email']).first()
        if user:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                token = generate_token(user)
                return Response({"token": token.token, "expires_in": token.expires, "scope": token.scope }, status=status.HTTP_200_OK)
        else:
            user = MyUser.objects.create(
                email=request.data['email'],
            )
            temp_password = randomword(18)
            user.set_password(temp_password)
            user.save()
            html = """http://%s/auth/ <br/> contraseña temporal: %s """%(request.META['HTTP_HOST'], temp_password)
            send_email("Bienvenido", user.email, html)
            return Response({"ok": True, "message": "Se ha enviado una contraseña temporal a su correo"}, status=status.HTTP_200_OK)

        return Response({"ok": False, "error": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)

class SuscriptionStore(APIView):
    def post(self, request, format=None):
        user = MyUser.objects.filter(email=request.data['email']).first()
        store = Store.objects.filter(id=request.data['store']).first()

        if user and store:
            suscription = StoreSuscription.objects.create(
                user=user,
                store=store,
            )
            data = StoreSuscriptionSerializer(suscription).data
            return Response({"ok": False, "message": "Suscripción creada con exito", "suscription": data}, status=status.HTTP_201_CREATED)
        
        return Response({"ok": False, "error": "Usuario o tienda no existen"}, status=status.HTTP_404_NOT_FOUND)

class SuscriptionUsers(APIView):
    def post(self, request, format=None):
        store = Store.objects.filter(id=request.data['store']).first()
        if store: 
            users_ids = list(set(store.suscriptions.all().values_list('user', flat=True)))
            users = MyUser.objects.filter(id__in=users_ids)
            data = MyUserSerializer(users, many=True).data
            print(data)
            return Response({"ok": False, "users": data}, status=status.HTTP_200_OK)

        return Response({"ok": False, "error": "Tienda no existen"}, status=status.HTTP_404_NOT_FOUND)