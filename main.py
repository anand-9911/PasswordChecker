import requests  # Allow us to make request.
import hashlib  # hash generator for SHA1 using builtin module
import sys


def request_api_data(query_char):
    pass
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # API USES HASHING
    # K anonimity- allows to recieve info to use personal data- we onlu give the first five characters of HASH
    # it will pick all the password that are hashed
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching:{res.status_code} check the api')
    return res


def pwned_api_check(password):
    # if encoded it will print b with the passed argument
    # hecdigest-> returns string object of double length contaning only hexa decimel digits
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    # print(first5_char, tail)
    # print(response)
    return get_password_leaks_count(response, tail)


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        # print(h, count)
        if h == hash_to_check:
            return count
    return 0


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} has been found used {count} many times, please change to a strong password')
        else:
            print(f'{password} is strong and you are good to GO')
    return 'Done!'


main(sys.argv[1:])
