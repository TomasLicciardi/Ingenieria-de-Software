import { Component } from '@angular/core';
import { UsuarioService } from 'src/app/services/usuario.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tablon',
  templateUrl: './tablon.component.html',
  styleUrls: ['./tablon.component.css']
})
export class TablonComponent {
  id_usuario = localStorage.getItem('id')
  arrayMensajes: any = [];
  mensaje: any = {
    "texto": ""
  };
  mensajeaEditar: any = {
    "texto": ""
  };

  constructor(
    private usuarioService: UsuarioService,
    private router: Router,
    ) {}

    ngOnInit() {
      this.usuarioService.getMensajesSeguidos(Number(this.id_usuario)).subscribe((data: any) => {
        // Crear una lista de promesas para todas las solicitudes de perfil
        const perfilPromises = data.map((mensaje: any) => {
          return this.usuarioService.getUsuarioPerfil(mensaje.id_usuario).toPromise().then((perfil: any) => {
            // Agregar el alias del perfil al mensaje
            mensaje.alias = perfil.alias;
          });
        });
        // Esperar a que todas las promesas se resuelvan
        Promise.all(perfilPromises).then(() => {
          this.arrayMensajes = data;
          console.log("Mensajes con alias de perfil:", this.arrayMensajes);
        }).catch(error => {
          console.error("Error al obtener perfiles:", error);
        });
      });
    }
     
//'%d/%m/%Y, %H:%M:%S'

  getFechaActual() {
    const now = new Date();
    const formattedDate = now.toLocaleDateString('es-AR', {
      day: 'numeric',
      month: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      second: 'numeric',
      hour12: false
    });
    return formattedDate;
  }

extractUsersAndTags(message: string): { users: string; tags: string } {
    const users = [];
    const tags = [];
  
    // Buscar usuarios con la expresión regular
    const userMatches = message.matchAll(/@(\w+)/g);
    for (const match of userMatches) {
      users.push(match[1]); // Captura el nombre de usuario
    }
  
    // Buscar etiquetas con la expresión regular
    const tagMatches = message.matchAll(/#(\w+)/g);
    for (const match of tagMatches) {
      tags.push(match[1]); 
    }
  
    return {
      users: users.length > 0 ? users.join(',') : '',
      tags: tags.length > 0 ? tags.join(',') : '' 
    };
  }

  publicar() {
    if(this.mensaje.texto.length>2){
      const { users, tags } = this.extractUsersAndTags(this.mensaje.texto);
      const mensajeCrear = {
        texto: this.mensaje.texto,
        menciones: users,
        etiqueta: tags,
        id_usuario: this.id_usuario,
        fecha: this.getFechaActual()
      };
      console.log("mensaje", mensajeCrear)
      this.usuarioService.postMensaje(mensajeCrear).subscribe((data:any) =>{
        console.log("Mensaje creado", data);
        this.ngOnInit();
      })
  }}
  
  
  editarMensaje(){
    const { users, tags } = this.extractUsersAndTags(this.mensajeaEditar.texto);
    const mensajeEditado = {
      texto: this.mensajeaEditar.texto,
      menciones: users,
      etiqueta: tags,
      id_usuario: this.id_usuario,
    };
    console.log("mensaje editado", mensajeEditado)
    this.usuarioService.putMensaje(this.mensajeaEditar.id,mensajeEditado).subscribe((data:any) =>{
      console.log("Mensaje editado", data);
      this.ngOnInit();
    })
  }

  botonMensajeEditar(mensaje: any){
    this.mensajeaEditar = mensaje;
  }
  
  eliminarMensaje(mensaje: any){
    this.usuarioService.deleteMensaje(mensaje.id).subscribe((data:any) =>{
      console.log("Mensaje eliminado", data);
      this.ngOnInit();
    })
  }
}
