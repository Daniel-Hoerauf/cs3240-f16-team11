import djclick as click
import requests
import json


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
    click.echo('Here is a list of your files:')
    # get files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_view_all_files/', {'username' : username})

    if r.status_code != 200:
        print('You do not currently have any reports. Goodbye.')
    else:
        json_str = r.text
        list = json.loads(json_str)
        reports_list = list['reports_list']

        for report in reports_list:
            print(report)

        view_file_contents(reports_list)


def view_file_contents(reports_list):
    if click.confirm('Do you want to display a report?'):
        fileName = click.prompt('Which report would you like to display?')
        click.echo(fileName) #test
        if click.confirm('Would you like to download this report? '):
            click.echo("yay!") #test


if __name__ == '__main__':
    login()