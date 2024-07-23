import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  url = '/api';

  constructor(private httpClient: HttpClient) { }

  getUsuarioPerfil(id: number){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpClient.get(`${this.url}/usuario/${id}`, { headers: headers });
  }

  postMensaje(mensajeData: any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpClient.post(`${this.url}/mensajes`, mensajeData, { headers: headers });
  }

  putMensaje(id: number, mensajeData: any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpClient.put(`${this.url}/mensaje/${id}`, mensajeData, { headers: headers });
  }

  deleteMensaje(id: number){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpClient.delete(`${this.url}/mensaje/${id}`, { headers: headers });
  }

  getMensajesSeguidos(id: number){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpClient.get(`${this.url}/usuario_seguidos_mensajes/${id}`, { headers: headers });
  }
}
