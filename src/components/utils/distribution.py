import random,math

def exponential(_lambda):
    U = random.uniform(0,1)
    return -(1/_lambda)*math.log(U)