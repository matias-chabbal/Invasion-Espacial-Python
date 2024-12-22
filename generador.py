

def generar_numero(num):
    cont = 1
    numero = 1
    while cont <= num:
        yield numero * 2
        cont += 1
        numero += 1

generar = generar_numero(10)

print(next(generar))
print('otro')
print(next(generar))
print(next(generar))