import djclick as click
import requests
import json
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from Crypto import Random

random_generator = Random.new().read


@click.command()
def login():
    click.echo('Please login.')
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    #authenticate user using requests - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_login/', data={'username': username, 'password': password})
    if(r.status_code == requests.codes.ok):
        view_files(username)
    else:
        click.echo('Invalid username and password')
        login()


def view_files(username):
    # get files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_view_all_files/', {'username' : username})

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
    #get report ID
    check = False
    report_id = 0
    for r in reports_list:
        if r['report_title'] == report_name:
            report_id = r['report_id']
            check = True
    if check == False:
        click.echo('No existing report with that name. Please enter another report.')
        view_report_contents(reports_list)
    else:
        # get report contents - CHANGE URL TO HEROKU AFTER DEVELOPMENT
        r = requests.post('http://127.0.0.1:8000/fda_view_report_contents/', {'report_id': report_id})
        if r.status_code == 200:
            json_str = r.text
            r_info = json.loads(json_str)
            report_info = r_info['report_info']
            #display report contents
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
                if report_info['files_encrypted'] == False:
                    check_encryption(report_info['files'], report_id, reports_list)
                else:
                    check_download(report_info['files'], report_id, reports_list)
        elif r.status_code == 404:
            click.echo('You do not currently have any reports. Goodbye.')
        else:
            click.echo('Error. Please contact site manager.')
            exit()


def check_encryption(files, report_id, reports_list):
    if click.confirm('Would you like to encrypt a file?'):
        file = click.prompt('Which file would you like to encrypt?')
        check = False
        for f in files:
            if f == file:
                check = True
        if check == False:
            click.echo('No existing file with that name.')
            check_encryption(files, report_id, reports_list)
        else:
            encrypt_file(files, report_id, reports_list)
    else:
        check_download(files, report_id, reports_list)


def check_download(files, report_id, reports_list):
    if click.confirm("Would you like to download a file from this report?"):
        file = click.prompt('Please enter the name of the file')
        check = False
        for f in files:
            if f == file:
                check = True
        if check == False:
            click.echo('No existing report with that name.')
            check_download(files, report_id, reports_list)
        else:
            download_files(report_id, reports_list)
    else:
        if click.confirm("Would you like to view another report's contents?"):
            view_report_contents(reports_list)
        else:
            click.echo('Goodbye then.')
            exit()


def encrypt_file(files, report_id, reports_list):
    # get report files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r1 = requests.post('http://127.0.0.1:8000/fda_get_files/', {'report_id': report_id})
    file_name = r1.headers['file_name']
    # open file
    file_contents = r1.content
    #encrypt contents
    key = RSA.generate(1024, random_generator)
    encrypted_data = key.publickey().encrypt(file_contents, 32)
    encoded_data = b64encode(encrypted_data[0])
    decoded_data = encoded_data.decode("utf-8")
    new_file_name = file_name + '.enc'
    new_file = open(new_file_name, 'w')
    new_file.write(decoded_data)
    new_file.close()
    #download file with private key
    pk_file_name = file_name.split('.')[0] + '.pem'
    pk_file = open(pk_file_name, 'wb')
    pk_file.write(key.exportKey())
    pk_file.close()
    click.echo('Success. File is now encrypted and downloaded.')
    click.echo('Please make sure to re-upload this encrypted file to your report.')

    if click.confirm("Do you want to encrypt another file?"):
        view_report_contents(reports_list)
    else:
        check_download(files, report_id, reports_list)


def download_files(report_id, reports_list):
    # get report files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_get_files/', {'report_id': report_id})

    if r.headers['encrypted'] == 'True':
        if click.confirm("Do you have the private key?"):
            key_file = click.prompt('Please enter the name of the file that includes the private key')
            key_str = open(key_file, 'rb').read()
            key = RSA.importKey(key_str.rstrip())
            decrypted_data = key.decrypt(b64decode(r.content))
            file_name = r.headers['file_name'].replace('.enc', '')
            file = open(file_name, 'wb')
            file.write(decrypted_data)
            file.close()
            click.echo('Success. Your file has been decrypted and downloaded.')
        else:
            click.echo('You cannot download the file.')
            if click.confirm("Would you like to view another report's contents?"):
                view_report_contents(reports_list)
            else:
                click.echo('Goodbye then.')
                exit()
    else:
        file_name = r.headers['file_name']
        file = open(file_name, 'wb')
        file.write(r.content)
        file.close()
        click.echo('Success. Your file has been downloaded.')

    if click.confirm("Would you like to view another report's contents?"):
        view_report_contents(reports_list)
    else:
        click.echo('Goodbye then.')
        exit()


if __name__ == '__main__':
    login()