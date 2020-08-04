import hashlib
import requests 
import sys

#Para hacer la peticion y comprobar que la respuesta es correcta.
def request_api(plain):
    url = 'https://api.pwnedpasswords.com/range/' + plain
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception('No se ha recibido la respuesta correcta')
    return res


#Para comprobar si hay coincidencias
def result(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


#Para hacer el hash
def hash5first(password):
    hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    five, tail = hashed[:5], hashed[5:]
    response = request_api(five)
    return result(response, tail)


def main(args):
    for password in args:
        count = hash5first(password)
        if count != 0:
            print(f'La contraseña {password} que has introducido se ha encontrado {count} veces')
        else:
            print(f'No se ha encontrado la contraseña {password} ninguna vez')

if '__name__' == '__main__':
    main(sys.argv[1:])