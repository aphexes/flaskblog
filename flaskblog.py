from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Derek Chen',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'June 23, 2022'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 24, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', comments=posts)
    # we are passing these posts into our home template and gaining access
    # to that variable in our home template as equal to our post data

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# this conditional is only true if we run the script with python directly;
# if we import the module to somewhere else, the name will be the name of the module
if __name__ == '__main__':
    app.run(debug=True)