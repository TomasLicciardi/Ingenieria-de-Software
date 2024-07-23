import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  url = '/api';
  constructor(
    private httpClient: HttpClient
  ) { }

  getUsarioPerfil(id:number) {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json',
  });
  return this.httpClient.get(`${this.url}/usuario/${id}`, { headers: headers });
}



}