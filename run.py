from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    # this conditional is only true if we run the script with python directly;
    # if we import the module to somewhere else, the name will be the name of the module
    app.run(debug=True)