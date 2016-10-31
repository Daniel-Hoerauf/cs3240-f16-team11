import djclick as click

@click.command()
def login():
    click.echo('Hello! Please login.')
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    # authenticate if username and password is valid - check database
    userFiles() #if valid user, call userFiles()

def userFiles():
    click.echo('Here is a list of your files:')
    # get files from database
    click.echo(click.format_filename(b'foo.txt')) #test

    if click.confirm('Do you want to view a specific report?'):
        fileName = click.prompt('Which report would you like to display?')
        # display chosen file
        click.echo(fileName) #test
        if click.confirm('Would you like to download this report? '):
            # download report
            click.echo("downloaded") #test

if __name__ == '__main__':
    login()