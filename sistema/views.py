from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

class Login(View):
    """Class Based View para autenticação de usuários"""
    def get(self, request):
        contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect("/veiculo")
        else:
            return render(request, 'autenticacao.html', contexto)
    
    def post(self, request):
        usuario=request.POST.get('usuario', None)
        senha=request.POST.get('senha', None)

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/veiculo")
            return render(request, "autenticacao.html", {'mensagem': 'Usuário Inativo.'})
        return render(request, 'autenticacao.html', {'mensagem':'Usuário ou Senha Inválidos!' })
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    
class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.get_full_name(),  # Usa o nome completo do usuário
            'email': user.email,
            'token': token.key
        })