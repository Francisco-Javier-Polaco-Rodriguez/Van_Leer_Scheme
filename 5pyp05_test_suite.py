# -*- coding: utf-8 -*-
"""5pyp05_test_suite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WR7cjGv7clExhZRM_fNQ8ns4Mci1R3VQ

Tests suit for Hyperbolic Conservations Laws
============================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square
from numba import jit
from tqdm import tqdm
"""# Support class"""

class TestHCL():
    """
    This is the support class for the 5 tests where are defined
    :param tag : index of the test (1 <= tag <= 5)
    :param tFinal : final time for the time integration of the equation
    :param domain : 2-elements tuple containing the domain of the simulation
    :param nx : number of grid points
    :param nu : ratio dt / dx which then define the time step
    :param flux : callable for the flux function
    :param u0 : callable for the initial u function
    :param uFinal : analytical profile of the solution at tFinal
    """
    def __init__(self, tag=None, tFinal=0, domain=(-1.0,+1.0), nx=0, nu=0.8, flux=lambda x :0, u0=lambda x:0, a=None):
        assert(isinstance(tag, int))
        assert(tag>0)
        assert(tag<=5)
        self.tag=tag
        self.time=tFinal
        self.domain=domain
        self.nx=nx
        self.nu=nu
        self.flux=flux
        self.u0=u0
        self.dx=(domain[1]-domain[0])/nx
        self.dt=nu*self.dx
        self.a=a
        self.x=np.linspace(domain[0], domain[1], nx)


    def __repr__(self):
        return f"""...................................................
{"Tag number":>24} : {self.tag}
{"Final time":>24} : {self.tFinal}
{"domain":>24} : {self.domain}
{"Number of grid points":>24} : {self.nx}
{"nu ":>24} : {self.nu}
{"dx ":>24} : {self.dx}
{"dt ":>24} : {self.dt}
{"a (wave speed) ":>24} : {self.a}"""

##INTEGRATOR VAN LEER


def Van_Leer_integrator(u0:np.array,dx,dt,flux,a,tFinal,epsilon = 1e-60):
    N = np.int32(tFinal/dt)
    r = np.zeros((u0.shape[0]))
    eta = np.zeros((u0.shape[0]))
    F_lax = np.zeros((u0.shape[0]))
    F_bea = np.zeros((u0.shape[0]))

    u = np.concatenate((u0[:,np.newaxis],np.zeros((u0.shape[0],N))),axis = 1)
    J = len(u0)
    for k in tqdm(range(1,N+1)):
        for j in range(J):
            if j == J-1:
                r[j] = (u[j,k-1]-u[j-1,k-1])/(u[0,k-1]-u[j,k-1] + epsilon)
                F_lax[j] = 0.5*(flux(u[0,k-1]) - flux(u[j-1,k-1])) - 0.5*a(u[j,k-1])**2*dx**-1*dt*(u[0,k-1]-2*u[j,k-1]+u[j-1,k-1])
            else:
                r[j] = (u[j,k-1]-u[j-1,k-1])/(u[j+1,k-1]-u[j,k-1] + epsilon)
                F_lax[j] = 0.5*(flux(u[j+1,k-1]) - flux(u[j-1,k-1])) - 0.5*a(u[j,k-1])**2*dx**-1*dt*(u[j+1,k-1]-2*u[j,k-1]+u[j-1,k-1])
            F_bea[j] = 0.5*(3*flux(u[j,k-1]) - 4*flux(u[j-1,k-1]) + flux(u[j-2,k-1])) - 0.5*a(u[j,k-1])**2*dx**-1*dt*(u[j,k-1]-2*u[j-1,k-1]+u[j-2,k-1])
        eta = (np.abs(r) + r)/(np.abs(r) + 1)
        u[:,k] = u[:,k-1] - dx**-1*dt*(F_lax+0.5*eta*(F_bea-F_lax))
    return u



"""# Test 1 :"""

class Test1(TestHCL):
    def __init__(self):
        super().__init__(tag=1, tFinal=30, nx=40, flux=lambda x:x, u0=lambda x:-np.sin(np.pi*x), a=lambda x:1)
        self.uFinal=self.u0(self.x)
        ### Integrator

t1=Test1()


"""# Test 2 :"""

class Test2(TestHCL):
    def __init__(self):
        def flux(x):
            third=1.0/3.0
            return 0.5*(1+square((x+third)*np.pi,duty=third))
        super().__init__(tag=2, tFinal=4, nx=40, flux=lambda x:x, u0=lambda x:flux(x), a=lambda x:1)
        self.uFinal=self.u0(self.x)

t2=Test2()


class Test3(TestHCL):
    def __init__(self):
        def flux(x):
            third=1.0/3.0
            return 0.5*(1+square((x+third)*np.pi,duty=third))
        super().__init__(tag=3, tFinal = 4, nx=600, flux=lambda x:x, u0=lambda x:flux(x), a=lambda x:1)
        self.uFinal=self.u0(self.x)
t3=Test3()

t3=Test3()


class Test4(TestHCL):
    def __init__(self):
        third=1.0/3.0
        def flux(x):
            return 0.5*(1+square((x+third)*np.pi,duty=third))
        super().__init__(tag=4, tFinal=0.6, nx=40, flux=lambda x:0.5*x*x, u0=lambda x:flux(x), a=lambda x:x)
        self.uFinal=c=np.piecewise(self.x, [self.x <= -third, ((-third < self.x) & (self.x <= -third+0.6)), ((-third+0.6 < self.x) & (self.x <= third+0.6)), self.x > 0.6], [lambda x:0, lambda x:(third+x)/0.6, lambda x:1, lambda x:0])

t4=Test4()



class Test5(TestHCL):
    def __init__(self):
        third=1.0/3.0
        def flux(x):
            return square((x+third)*np.pi,duty=third)
        super().__init__(tag=5, tFinal=0.3, nx=40, flux=lambda x:0.5*x*x, u0=lambda x:flux(x), a=lambda x:x)
        self.uFinal=c=np.piecewise(self.x, [self.x <= -third-0.3, ((-third-0.3 < self.x) & (self.x <= -third+0.3)), ((-third+0.3 < self.x) & (self.x <= third)), self.x > third], [lambda x:-1, lambda x:10*third*x+1+0.3*third, lambda x:1, lambda x:-1])

t5=Test5()

tests = [t1,t2,t3,t4,t5]
N_time = 100

for test in tests:
    u0 = np.array(test.u0(np.linspace(-1,+1,test.nx)))
    x = test.x
    u = Van_Leer_integrator(u0,test.dx,test.dt,test.flux,test.a,N_time)
    plt.plot(x,u[:,-1],'r-',label = 'final u')    
    plt.plot(x,u0,'k',label = 'initial u')
    plt.legend()

    plt.show()
