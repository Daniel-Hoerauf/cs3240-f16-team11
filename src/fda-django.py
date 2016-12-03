import djclick as click
import requests
from requests.auth import HTTPBasicAuth

@click.command()
def login():
    click.echo('Please login.')
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    #authenticate user using requests - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_login/', data={'username': username, 'password': password})
    if(r.status_code == requests.codes.ok):
        userFiles()
    else:
        click.echo('Invalid username and password')
        login()

def userFiles():
    click.echo('Here is a list of your files:')
    # get files
    click.echo(click.format_filename(b'foo.txt')) #test

    if click.confirm('Do you want to display a report?'):
        fileName = click.prompt('Which report would you like to display?')
        click.echo(fileName) #test
        if click.confirm('Would you like to download this report? '):
            click.echo("yay!") #test

if __name__ == '__main__':
    login()