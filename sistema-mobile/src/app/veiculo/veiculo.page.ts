import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, LoadingController, NavController } from '@ionic/angular';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Usuario } from '../home/usuario.model';
import { Veiculo } from './veiculo.models';
import { ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-veiculo',
  templateUrl: './veiculo.page.html',
  styleUrls: ['./veiculo.page.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, IonicModule], // Inclua IonicModule aqui
  providers: [HttpClient, Storage]
})

export class VeiculoPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public lista_veiculos: Veiculo[] = [];

  constructor(
    public http: HttpClient,
    private storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
  ) { }

  async ngOnInit() {
    // Inicializa o armazenamento e obtém o usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    // Verifica se o usuário está autenticado, caso contrário redireciona para a página de login
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
    } else { 
      this.controle_navegacao.navigateRoot('/home');
    }

    // Após a inicialização, consulta os veículos
    this.consultarVeiculosSistemaWeb();
  }

  // Método para consultar a lista de veículos na API do Django
  async consultarVeiculosSistemaWeb() {
    // Exibe o carregamento enquanto a requisição é feita
    const loading = await this.controle_carregamento.create({
      message: 'Pesquisando....',
      duration: 60000 // Tempo máximo de espera (em milissegundos)
    });
    await loading.present();

    // Cabeçalho da requisição com o token de autenticação
    const http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Token ${this.usuario.token}` // Usando o token do usuário autenticado
    });

    // Faz a requisição GET para a API de veículos
    this.http.get('http://127.0.0.1:8000/veiculo/api/', { headers: http_headers })
      .subscribe({
        next: async (resposta: any) => {
          console.log(resposta); // Log para verificar a resposta da API
          this.lista_veiculos = resposta; // Atribui os veículos retornados à variável
          await loading.dismiss(); // Dismiss após a requisição
        },
        error: async (erro: any) => {
          await loading.dismiss(); // Dismiss caso ocorra erro
          const message = await this.controle_toast.create({
            message: `Falha ao consultar veículos: ${erro.message}`,
            cssClass: 'ion-text-center',
            duration: 2000
          });
          message.present(); 
        }
      });
  }
}
