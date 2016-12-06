import djclick as click
import requests
import json
# from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
from struct import pack, unpack, calcsize
from os.path import getsize
from base64 import b64encode, b64decode


random_generator = Random.new().read


@click.command()
def login():
    click.echo('Please login.')
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    # authenticate user using requests - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_login/', data={'username': username, 'password': password})
    if(r.status_code == requests.codes.ok):
        if click.confirm('Would you like to encrypt a file?'):
            encrypt_file()
        view_files(username)
    else:
        click.echo('Invalid username and password')
        login()


def view_files(username):
    # get files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_view_all_files/',
                      {'username': username})

    if r.status_code == 200:
        json_str = r.text
        list = json.loads(json_str)
        reports_list = list['reports_list']

        click.echo('Here is a list of your reports:')
        for report in reports_list:
            click.echo(report['report_title'])

        if click.confirm('Do you want to display a report?'):
            view_report_contents(reports_list)
        else:
            click.echo('Goodbye then.')
            exit()
    elif r.status_code == 404:
        click.echo('You do not currently have any reports. Goodbye.')
    else:
        click.echo('Error. Please contact site manager.')
        exit()


def view_report_contents(reports_list):
    report_name = click.prompt('Which report would you like to display?')
    # get report ID
    check = False
    report_id = 0
    for r in reports_list:
        if r['report_title'] == report_name:
            report_id = r['report_id']
            check = True
    if check is False:
        click.echo('No existing report with that name. Please enter another report.')
        view_report_contents(reports_list)
    else:
        # get report contents - CHANGE URL TO HEROKU AFTER DEVELOPMENT
        r = requests.post('http://127.0.0.1:8000/fda_view_report_contents/', {'report_id': report_id})
        if r.status_code == 200:
            json_str = r.text
            r_info = json.loads(json_str)
            report_info = r_info['report_info']
            # display report contents
            click.echo('Title: ' + report_info['title'])
            click.echo('Owner: ' + report_info['owner'])
            click.echo('Short Description: ' + report_info['short_desc'])
            click.echo('Summary: ' + report_info['long_desc'])
            click.echo('Shared With: ' + report_info['shared_with'])
            click.echo('Created: ' + report_info['timestamp'])

            click.echo('Files: ')
            for r in report_info['files']:
                click.echo(r)

            if report_info['files'] == []:
                if click.confirm("Would you like to view another report's contents?"):
                    view_report_contents(reports_list)
                else:
                    click.echo('Goodbye then.')
                    exit()
            else:
                check_download(report_info['files'], report_id,
                               reports_list, report_info['files_encrypted'])
        elif r.status_code == 404:
            click.echo('You do not currently have any reports. Goodbye.')
        else:
            click.echo('Error. Please contact site manager.')
            exit()

def check_download(files, report_id, reports_list, files_encrypted):
    if click.confirm("Would you like to download a file from this report?"):
        file = click.prompt('Please enter the name of the file')
        check = False
        for f in files:
            if f == file:
                check = True
        if check is False:
            click.echo('No existing report with that name.')
            check_download(files, report_id, reports_list)
        else:
            download_files(report_id, reports_list, file, files_encrypted)
    else:
        if click.confirm("Would you like to view another report's contents?"):
            view_report_contents(reports_list)
        else:
            click.echo('Goodbye then.')
            exit()


def encrypt_file():
    key = random_generator(256)
    file_name = click.prompt('Enter the path of the file you wish to encrypt')
    encrypt(file_name, key)
    pk_file_name = file_name + '.pem'
    with open(pk_file_name, 'wb') as f:
        f.write(b64encode(key))
    exit()

def download_files(report_id, reports_list, file_name, files_encrypted):
    # get report files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_get_files/',
                      {'report_id': report_id,
                       'file_name': file_name})
    if files_encrypted:
        if click.confirm("Do you have the private key?"):
            key_file = click.prompt('Enter the path to the RSA key for this file')
            key = None
            with open(key_file, 'rb') as f:
                key = b64decode(f.read())
            out_name = file_name
            if file_name.split('.')[-1] == 'enc':
                out_name = file_name[:-4]
            decrypt_file(file_name, key, out_name)
            click.echo('File saved as {}'.format(out_name))
            exit()
        else:
            click.echo('You cannot download the file.')
            if click.confirm("Would you like to view another report's contents?"):
                view_report_contents(reports_list)
            else:
                click.echo('Goodbye then.')
                exit()
    else:
        file = open(file_name, 'wb')
        file.write(r.content)
        file.close()
        click.echo('Success. Your file has been downloaded.')

    if click.confirm("Would you like to view another report's contents?"):
        view_report_contents(reports_list)
    else:
        click.echo('Goodbye then.')
        exit()


def encrypt(file_name, sym_key):
    '''Uses the supplied key and AES encryption to encrypt a file'''
    key = SHA256.new(sym_key).digest()
    out_file_name = '{}.enc'.format(file_name)
    iv = Random.new().read(AES.block_size)
    filesize = getsize(file_name)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(file_name, 'rb') as read_file:
        with open(out_file_name, 'wb') as out_file:
            out_file.write(pack('<Q', filesize))
            out_file.write(iv)
            while True:
                chunk = read_file.read(2048)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b'\x00' * (16 - (len(chunk) % 16))

                out_file.write(cipher.encrypt(chunk))
    return True


def decrypt_file(file_name, sym_key, out_file_name):
    '''Decrypt the AES encrypted file'''
    key = SHA256.new(sym_key).digest()
    with open(file_name, 'rb') as read_file:
        # Gets the first `long` from the file
        size = unpack('<Q', read_file.read(calcsize('Q')))[0]
        iv = read_file.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(out_file_name, 'wb') as out_file:
            while True:
                chunk = read_file.read(2048)
                if len(chunk) == 0:
                    break
                out_file.write(cipher.decrypt(chunk))
            out_file.truncate(size)
        return True


if __name__ == '__main__':
    login()
