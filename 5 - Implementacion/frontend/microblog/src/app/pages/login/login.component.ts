import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import jwtDecode, {JwtDecodeOptions} from 'jwt-decode';


@Component ({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
  loginForm!: FormGroup;
  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
   ) {}

   ngOnInit() {
    this.loginForm = this.formBuilder.group({
      mail: ['', Validators.required],
      contrasena: ['', Validators.required]
    })
   }
  
  login(dataLogin:any = {}){ 
  //   dataLogin = {email: "tiago4@gmail.com", contraseña: "1234"}
    console.log('Comprobando credenciales');
    this.authService.login(dataLogin).subscribe({
      next: (rta:any) => {
        console.log('Respuesta login: ',rta.access_token);
        localStorage.setItem('token', rta.access_token);
        var decodedPayload: any = jwtDecode(rta.access_token);
        var usuarioId = decodedPayload['sub']['id'];
        localStorage.setItem('id', usuarioId );
        this.router.navigate(['/tablon']);
      },
          error:(error) => {
          alert('Credenciales incorectas');
          localStorage.removeItem('token');
          localStorage.removeItem('id')
      }, complete: () => {
        console.log('Finalizado');
      }
    })
  }

  submit() {
    if(this.loginForm.valid) {
      console.log('Form login: ',this.loginForm.value);
      this.login(this.loginForm.value)
    } else {
      alert('Formulario invalido');
    }
  }

  mostrarAlerta(){
    alert("Si olvidaste tu contraseña comunicate con la administracion para restablecerla");
  }
}