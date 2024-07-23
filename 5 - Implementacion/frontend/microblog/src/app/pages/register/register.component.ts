import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm!: FormGroup;
  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder,
    
    ) {}
    ngOnInit() {
      this.registerForm = this.formBuilder.group({
        alias: ['', Validators.required],
        nombre: ['', Validators.required],
        mail: ['', Validators.required],
        foto: [''],
        contrasena: ['', Validators.required],
        descripcion: ['', Validators.required]

      })
     }

  register(formData: any) {
    this.authService.register(formData).subscribe(
      (response) => {
        alert("Registro exitoso");
        this.router.navigate(['/login']);
      },
      (error) => {
        alert("Registro fallido");
      }
    );
  }


  submit() {
    if(this.registerForm.valid) {
      console.log('Form login: ',this.registerForm.value);
      this.register(this.registerForm.value)
    } else {
      alert('Formulario invalido');
    }
  }

}




