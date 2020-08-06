from flask import render_template,request,Blueprint,url_for,flash,redirect,abort
from flask_login import current_user,login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
# we create instance of this blueprint
posts=Blueprint('posts',__name__) # 'users' is the name of our blueprint

@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form,legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    # this following line says give me post with current post_id and if it doesnt exist then return 404 page
    # but if the page does exist then render the page that we want
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content= form.content.data
        # no need to do db.session.add() since they are already in the database
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post',
                           legend='Update Post', form=form)

@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

