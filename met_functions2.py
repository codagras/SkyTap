def PHYCON():
    import os
    os.environ['Tko'] = str(273.15)
    os.environ['R'] = str(8.3144)
    os.environ['Rd'] = str(287.05)
    os.environ['Rv'] = str(461.51)
    os.environ['po'] = str(100000)
    os.environ['epsilon'] = str(0.622)
    os.environ['Cpd'] = str(1005.2)
    os.environ['Cpv'] = str(1870.4)
    os.environ['Cl'] = str(4218.0)
    os.environ['Ci'] = str(2106.0)
    os.environ['Lvo'] = str(2500800)
    os.environ['Lso'] = str(2834500)
    os.environ['rhol'] = str(1000)
    os.environ['eso'] = str(610.7)
    os.environ['g'] = str(9.81)

def es(Tk):
    import math
    eso = 610.7
    Lvo = 2500800.0
    Cl = 4218.0
    Cpv = 1870.4
    Tko = 273.15
    Rv = 461.51
    result = eso*math.exp(((Lvo+(Cl - Cpv)*Tko)*(1.0/Tko - 1.0/Tk) -(Cl - Cpv)*math.log(Tk/Tko))/Rv)
    return(result)

def ws(Tk, P):
    epsilon = 0.622
    result = epsilon*es(Tk)/(P - es(Tk))
    return(result)

def lv(Tk):
    Lvo = 2500800.0
    Cl = 4218.0
    Cpv = 1870.4
    lv = (Lvo - (Cl - Cpv)*(Tk - 273.15))
    return(lv)

def reverse_ei(Tk):
    import math
    eso = 610.7
    Lso = 2834500
    Ci = 2106.0
    Cpv = 1870.4
    Tko = 273.15
    Rv = 461.51
    result = (eso*math.exp(((Lso+(Ci - Cpv))*(1.0/Tko - 1.0/Tk) - (Ci - Cpv)*math.log(Tk/Tko))/Rv) - e)
    return(result)

def frostpoint(Tdk):
    import math
    import scipy.optimize
    global e
    e  = es(Tdk)
    fp = scipy.optimize.newton(reverse_ei, 273.15, tol=1e-08)
    return(fp)

def reverse_h(x):
    Cpd = 1005.2
    Cl = 4218.0
    global h
    ws0 = ws(x[0], p)
    return(h - (Cpd + (ws0 + x[1])*Cl)*x[0] - lv(x[0])*ws0, w - x[1] - ws0)

def thermo_wetbulb(Tk, Tdk, Pa):
    import scipy.optimize
    epsilon = 0.622
    Cpd = 1005.2
    Cl = 4218.0
    global p
    global w
    global h
    p = Pa
    e = es(Tdk)
    w = epsilon*e/(p - e)
    h = (Cpd + w*Cl)*Tk + lv(Tk)*w
    result = scipy.optimize.fsolve(reverse_h, [Tk, w], xtol=1e-08)
    return(result[0])

def eval_td(Tk):
    eso = 610.7
    Lvo = 2500800.0
    Cl = 4218.0
    Cpv = 1870.4
    Tko = 273.15
    Rv = 461.51
    import math
    return(eso*math.exp(((Lvo+(Cl - Cpv)*Tko)*(1.0/Tko - 1.0/Tk) - (Cl - Cpv)*math.log(Tk/Tko))/Rv) - x)

def e_to_td(e):
    import scipy.optimize
    global x
    x = e
    td = scipy.optimize.newton(eval_td, 273.15, tol=1e-08)
    return(td)
    
    
