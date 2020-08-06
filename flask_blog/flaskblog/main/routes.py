from flask import render_template,request,Blueprint
from flaskblog.models import Post

# we create instance of this blueprint
main=Blueprint('main',__name__) # 'users' is the name of our blueprint

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page',1,type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=posts)

@main.route('/about')
def about():
    return render_template('about.html',title='About')

# abc@gmail.com
# qwerty123
