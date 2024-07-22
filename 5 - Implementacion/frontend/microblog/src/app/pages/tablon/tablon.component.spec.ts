import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TablonComponent } from './tablon.component';

describe('TablonComponent', () => {
  let component: TablonComponent;
  let fixture: ComponentFixture<TablonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TablonComponent]
    });
    fixture = TestBed.createComponent(TablonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
