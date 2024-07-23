import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  idUsuario = Number(localStorage.getItem("id"))
    usuario:any = {
      "alias": ""
    };  
  constructor(
    private authService: AuthService,
    private usuarioService: UsuarioService,  
  ){}

  ngOnInit(): void {
    this.usuarioService.getUsuarioPerfil(this.idUsuario).subscribe(
      (data) => {
        this.usuario = data;
      },
      (error) => {
        console.error('Error fetching user profile', error);
      }
    );
  }

  cerrarSesion(){
  this.authService.logout();
  }
}
