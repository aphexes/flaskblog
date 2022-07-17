from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)    # default page set to 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # date_posted.desc() gives us our posts from latest to oldest
    # page=page is how we send a selected page to our query
    # this grabs the posts and displays them on the home screen
    return render_template('home.html', posts=posts)
    # we are passing these posts into our home template and gaining access
    # to that variable in our home template as equal to our post data

@main.route("/about")
def about():
    return render_template('about.html', title='About')
