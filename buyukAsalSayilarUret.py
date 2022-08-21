from random import randrange, getrandbits

def asal_kontrol(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    # Miller–Rabin asallık testi
    for i in range(k):
        # rastgele sayı seçiliyor
        a = randrange(2, n - 1)
        # a=n(mod r) hesaplanıyor
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                # x=n(mod 2) hesaplanıyor
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def asal_sayi_aday_uret(uzunluk):
    p = getrandbits(uzunluk)
    p = p | (1 << uzunluk - 1) | 1
    return p


def asal_sayi_uret(uzunluk, haric = 1):
    p = 4
    while not asal_kontrol(p, 128) and haric != p:
        p = asal_sayi_aday_uret(uzunluk)
    return p