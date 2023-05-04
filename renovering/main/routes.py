from flask import Blueprint, render_template, request, flash
from renovering.models import Post 

main = Blueprint('main', '__name__')

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if posts.total == 0:
        flash('Det finns inga renoveringar att visa. Ännu.', 'warning')

    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
