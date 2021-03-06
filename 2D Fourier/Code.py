# The presented code is a fragment thus it cannot be run as is.

def esdf():
    global N1, N2, T, S, X, Y, l, wc1, wc2, rr
    #forming ESDF
    formula = f1_e1.get() #getting formula string from the edit box
    code = parser.expr(formula).compile()
    N1 = int(f1_e2_1.get()) #getting parameters from boxes too
    N2 = int(f1_e2_2.get())
    T = float(f1_e3.get())
    wc1 = int(f1_e4.get())
    wc2 = int(f1_e5.get())
    #Processing cutoff frequencies
    if (wc1 == 0):
        wc1 = N1
    if (wc2 == 0):
        wc1 = N2
    #Prepping the matrix
    S = np.zeros([N1, N2], dtype=float)
    l = 2
    #Filling an array by compiling formula
    for w1 in range(0, wc1):
        for w2 in range(0, wc2):
            S[w1, w2] = eval(code)
    X, Y = np.meshgrid(np.arange(N2), np.arange(N1))
    ax2.clear()
    ax2.plot_surface(X, Y, S, cmap=cm.binary, edgecolor='black')
    ch2.draw()

def simulation():
    global sig
    global Xfe
    #Forming coefficients
    if (wc1<N1 or wc2<N2): #limited ESDF
        coefs = 100
        Xfe = np.zeros([coefs, coefs], dtype=float)
        for k1 in range(1, coefs):
            for k2 in range(1, coefs):
                Xfe[k1, k2] = math.sqrt(1/(T*N1*T*N2*(1+l*l)))
        Xfe[0, 0] = 1/math.sqrt(T*N1*T*N2)
        for k1 in range(0, coefs):
            Xfe[k1, 0] = math.sqrt(1/(T*N1*(1+l*l)))
            Xfe[0, k1] = math.sqrt(1/(T*N2*(1+l*l)))
        #Random/determined coefficients
        import random
        r1 = np.zeros([N1, N2], dtype=int)
        r2 = np.zeros([N1, N2], dtype=int)
        for m1 in range(0, N1):
            for m2 in range(0, N2):
                if (reg == 1):
                    r1[m1,m2] = random.choice((-1, 1))
                    r2[m1,m2] = random.choice((-1, 1))
                else:
                    r1[m1,m2] = 1
                    r2[m1,m2] = 1
    else: #unlimited ESDF
        coefs = 100
        Xfe = np.zeros([coefs, coefs], dtype=float)
        for k1 in range(1, N1-1):
            for k2 in range(1, N2-1):
                Xfe[k1, k2] = math.sqrt(S[int(math.pi * k1 / (N1-1)), int(math.pi * k2 / (N2-1))] /T/(N1-1)/T/(N2-1))
        Xfe[0, 0] = math.sqrt(S[0,0] / T / T / (N1-1) / (N2-1))
        for n in range(1, N1-1):
            Xfe[n, 0] = math.sqrt(S[int(math.pi * n / (N1-1)), 0] / 2 / (N1-1))
        for n in range(1, N2-1):
            Xfe[0, n] = math.sqrt(S[0, int(math.pi * n / (N2-1))] / 2 / (N2-1))
        Xfe = Xfe/4
        #Rand/det coefs
        import random
        r1 = np.zeros([N1, N2], dtype=int)
        r2 = np.zeros([N1, N2], dtype=int)
        for m1 in range(0, N1):
            for m2 in range(0, N2):
                if (reg == 1):
                    r1[m1,m2] = random.choice((-1, 1))
                    r2[m1,m2] = random.choice((-1, 1))
                else:
                    r1[m1,m2] = 1
                    r2[m1,m2] = 1
    #Simulation
    sig = np.zeros([N1, N2], dtype=complex)
    sig_ = np.zeros([N1, N2], dtype=float)
    co = 1j
    for i1 in range(0, N1):
        for i2 in range(0, N2):
            sig[i1, i2] += r1[0,0]*Xfe[0, 0]
            for n in range(1, int((N1-1)/2)):
                sig[i1, i2] += (r1[n,0] - co * r2[n,0]) * Xfe[n, 0] * cmath.exp(co * 2 * math.pi / N1 * n * i1)
                sig[i1, i2] += (r1[n,0] + co * r2[n,0]) * Xfe[n, 0] * cmath.exp(co * 2 * math.pi / N1 * n * i1)
            for m in range(1, int((N2-1)/2)):
                sig[i1, i2] += (r1[0,m] - co * r2[0,m]) * Xfe[0, m] * cmath.exp(co * 2 * math.pi / N2 * m * i2)
                sig[i1, i2] += (r1[0,m] + co * r2[0,m]) * Xfe[0, m] * cmath.exp(co * 2 * math.pi / N2 * m * i2)
            for k1 in range(1, int((N1-1)/2)):
                for k2 in range(1, int(N2 - 1)):
                    sig[i1, i2] += (r1[k1,k2] - co * r2[k1,k2]) * Xfe[k1, k2] * cmath.exp( co *  2*math.pi * (k1*i1/N1+k2*i2/N2))
                    sig[i1, i2] += (r1[k1,k2] + co * r2[k1,k2]) * Xfe[k1, k2] * cmath.exp( co *  2*math.pi * (k1*i1/N1+k2*i2/N2))
            sig_[i1,i2] = math.sqrt(sig.real[i1,i2]*sig.real[i1,i2] + sig.imag[i1,i2]*sig.imag[i1,i2])
(sig.imag*sig.imag))
    sig = sig_
    ax3.clear()
    ax3.plot_surface(X, Y, sig_, cmap=cm.binary, edgecolor='black')
    ch3.draw()
