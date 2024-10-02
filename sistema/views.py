from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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