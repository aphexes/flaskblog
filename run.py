from flaskblog import app

# this conditional is only true if we run the script with python directly;
# if we import the module to somewhere else, the name will be the name of the module
if __name__ == '__main__':
    app.run(debug=True)