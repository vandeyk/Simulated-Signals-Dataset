FurierKernel::FurierKernel()	{ }

FurierKernel::FurierKernel(int p, int n, int N){
    dim = N;
    PaliMatrix pali(p, n, N); // Создание объекта класса матрицы базиса ВКФ-Пэли
    DefMatrix def(N); // Создание объекта класса матрицы базиса ДЭФ

    fill = new complex<float> * [N];
    for (int j = 0; j < N; j++){
        fill[j] = new complex<float>[N];
    }

    for (int k=0; k<N; k++){
        for(int m=0; m<N; m++){

            fill[k][m] = makeComplex(def, pali, N, k, m);
        }
    }
}

complex<float> FurierKernel::makeComplex(DefMatrix def, PaliMatrix pali, int N, int k, int m){
    //round(re*100)/100
    complex<float> buf(0,0);
    for (int i=0; i < N; i++){
        buf += def.getElement(m,i)*conj(pali.getElement(k,i));
    }
    float re = round((buf.real()/N)*100)/100;
    float im = round((buf.imag()/N)*100)/100;
    complex<float> result(re, im);
    return result;
}
void FurierKernel::print(){
    int i,j;
    for (i=0;i<dim;i++){
        for(j=0;j<dim;j++){
            cout << fill[i][j];
        }
        cout <<  endl;
    }
}
complex<float> FurierKernel::getElement(int m, int i){
   return fill[m][i];
}
