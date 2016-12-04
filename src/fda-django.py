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
    # get files - CHANGE URL TO HEROKU AFTER DEVELOPMENT
    r = requests.post('http://127.0.0.1:8000/fda_view_all_files/', {'username' : username})

    if r.status_code == 200:
        json_str = r.text
        list = json.loads(json_str)
        reports_list = list['reports_list']

        click.echo('Here is a list of your files:')
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


def view_report_contents(reports_list):
    report_name = click.prompt('Which report would you like to display?')
    #get report ID
    report_id = 0
    for r in reports_list:
        if r['report_title'] == report_name:
            report_id = r['report_id']
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
        click.echo('Files: ' + report_info['files'])

        if click.confirm("Would you like to download this report's files?"):
            # fda_download_files()
            click.echo('download files')
        else:
            if click.confirm("Would you like to view another report's contents?"):
                view_report_contents(reports_list)
            else:
                click.echo('Goodbye then.')
                exit()
    elif r.status_code == 404:
        click.echo('You do not currently have any reports. Goodbye.')
    else:
        click.echo('Error. Please contact site manager.')


if __name__ == '__main__':
    login()