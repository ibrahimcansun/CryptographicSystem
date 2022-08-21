import random
import buyukAsalSayilarUret

# ürettiği şifreli kodları aynı public/private key için bir daha üretmemesi adına bellekte tutan değişkenler
kodArsivPublic = {}
kodArsivPrivate = {}

def genisletilmis_oklid(a, b):
	x0, x1, y0, y1 = 0, 1, 1, 0

	while a != 0:
		q, b, a = b//a, a, b%a
		y0, y1 = y1, y0 - q*y1
		x0, x1 = x1, x0 - q*x1

	return b, x0, y0

def publicKeyUret(totient):
	public_key = random.randrange(3, totient)
	# ebob 1 olana kadar rastgele üretilen public_key değerini arttır
	while not buyukAsalSayilarUret.asal_kontrol(public_key):
		public_key += 1
	return public_key


def privateKeyUret(public_key, totient):
	# genişletilmiş öklid methodu yardımıyla büyük sayılarda çok daha hızlı private key üretilir
	g, _, private_key = genisletilmis_oklid(int(totient), int(public_key))
	if private_key > totient:
		private_key = private_key % totient
	elif private_key < 0:
		private_key += totient
	return private_key

def RSA(bit):
	global kodArsivPublic, kodArsivPrivate
	p = buyukAsalSayilarUret.asal_sayi_uret(bit)
	q = buyukAsalSayilarUret.asal_sayi_uret(bit, p) # p ve q eşit olmaması için p'yi hariç olarak gönderiyoruz
	n = p*q
	totient = (p-1)*(q-1)
	public_key = publicKeyUret(totient)
	private_key = privateKeyUret(public_key, totient)
	# print("Prime numbers are\np : ", p, "\nq : ", q)
	# print("Modulus : ", n)
	# print("Euler's Totient : ", totient)
	# print("Public key: ", public_key)
	# print("Private key: ", private_key)
	# değişkenleri sıfırla
	kodArsivPublic = {}
	kodArsivPrivate = {}
	return (n, public_key), (n, private_key)


def sifrele(mesaj, key):
	n, public_key = key

	global kodArsivPublic
	if public_key not in kodArsivPublic.keys():
		kodArsivPublic[public_key] = {}
	sifre_listesi = []
	for c in mesaj:
		kod = ord(c)
		if kod in kodArsivPublic[public_key].keys():
			sifreli_kod = kodArsivPublic[public_key][kod]
		else:
			sifreli_kod = str(pow(kod, public_key, n))
			kodArsivPublic[public_key][kod] = sifreli_kod
		sifre_listesi.append(sifreli_kod)
	return ' '.join(sifre_listesi)

def sifre_coz(sifrelenmis_mesaj, key):
	n, private_key = key

	global kodArsivPrivate
	cozulmus_mesaj = ""
	sifre_listesi = sifrelenmis_mesaj.split(' ')
	for sifreli_kod in sifre_listesi:
		if sifreli_kod in kodArsivPrivate.keys():
			kod = kodArsivPrivate[sifreli_kod]
		else:
			kod = (pow(int(sifreli_kod), private_key, n))
			kodArsivPrivate[sifreli_kod] = kod
		cozulmus_mesaj += chr(kod)
	return cozulmus_mesaj


# if __name__ == '__main__':
# 	bit = int(input("Bit: "))
# 	public_key, private_key = RSA(bit)
# 	while True:
# 		mesaj = input("Mesaj: ")
# 		sifrelenmis_mesaj = sifrele(mesaj, public_key)
# 		print("Şifrelenmiş Mesaj:", sifrelenmis_mesaj)
# 		cozulmus_mesaj = sifre_coz(sifrelenmis_mesaj, private_key)
# 		print("Çözülmüş Mesaj:", cozulmus_mesaj)

