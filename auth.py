from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from forms import PostForm, LoginForm, SignupForm
from models import db, Posts, Users
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from flask import current_app as app

auth = Blueprint("auth", __name__, template_folder="../templates")

# #CRUD
    
#admin page and save posts to db
@auth.route("/admin", methods=["GET", "POST"])
def post():
    headline = None
    textarea = None
    snippet = None
    image = None
    form = PostForm()

     #manage posts and file upload from admin page
    if form.validate_on_submit():
        #check if user is logged in
        if 'user_id' in session:
            #manage upload of posts without attached files
            if form.image.data.filename == '':
                post = Posts(form.headline.data, form.textarea.data, form.snippet.data, form.image.data.filename)
                db.session.add(post)
                db.session.commit()
                return render_template("admin.html",
                    form = form,
                    posts=Posts.query.all()
                    )
            
            #manage uploads of posts with file
            if request.files['image']:
                image = request.files['image']
                filename = secure_filename(form.image.data.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                post = Posts(form.headline.data, form.textarea.data, form.snippet.data, filename)
                db.session.add(post)
                db.session.commit()
                return render_template("admin.html",
                                    form = form,
                                    posts=Posts.query.all()
                                    )
        else:
            flash('Redirected to login')
            return redirect("login", 302) 


    if request.method=="GET":
        if 'user_id' in session:
            return render_template("admin.html",
                                headline = headline,
                                textarea = textarea,
                                snippet = snippet,
                                image = image,
                                form = form,
                                posts=Posts.query.all()
                                )
        else:
            flash('Redirected to login')
            return redirect("login", 302)
        

#user signup
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method=="GET":
        return render_template("signup.html",
                            form = form
                            )
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None

        if not username:
            error = "Username is required"
        
        if not password:
            error = "Password is required"

        if error is None:   
            try: 
                hashed_pw = generate_password_hash(password)
                user = Users(username, hashed_pw)
                form.username.data = ""
                form.password.data = ""
                db.session.add(user)
                db.session.commit()
                #TODO: redirecting to login after signup not working yet
                return render_template("login.html",
                                    form = LoginForm()
                                    )
            #db.IntegrityError did not work so changed for exc
            #TODO: flash does not get shown in frontend yet
            except exc.IntegrityError:
                flash(f"User {username} already exists")
        else:
            return render_template("login.html",
                               form = LoginForm())
                
        flash(error)

    return render_template("signup.html",
                            form = form,
                            message = "Registration failed"
                            )


#admin login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        flash('Already logged in, redirect to admin page')
        return redirect('admin')
    form = LoginForm()
    if request.method=="GET": 
        return render_template("login.html",
                                form=form
                                )
    #validate form
    if request.method=="POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            error = None

            user = Users.query.filter_by(username=username).first()

            if user is None:
                error = "Incorrect username"
                flash(error)
                return redirect("login", 302)
            elif not check_password_hash(user.password, password):
                error = "Incorrect password"
                flash(error)
                return redirect("login", 302)

            if error is None:
                session.clear()
                session["user_id"] = user["_id"]
                return redirect("admin", 302)
        else:
            return redirect("login", 302)

#single post view for update
@auth.route("/update_post_view/<post_id>", methods=["POST", "GET"])
def update_post_view(post_id):
    form = PostForm()
    if request.method=="GET": 
        if 'user_id' in session:
            post = Posts.query.filter_by(_id=post_id).first()

            #populate form with data from post
            form.headline.data = post.headline
            form.snippet.data = post.snippet
            form.textarea.data = post.textarea
            return render_template("update_post_view.html",
                                form=form,
                                post=post)

        else:
            flash('Redirected to login')
            return redirect(url_for("auth.admin"))
    #update post
    if form.validate_on_submit():
        #check if user is logged in
        if 'user_id' in session:
            #manage update of posts
            post = Posts.query.filter_by(_id=post_id).first()
            post.headline = form.headline.data
            post.snippet = form.snippet.data
            post.textarea = form.textarea.data
            #TODO: works with first time upload but not with posts who already have an image
            if request.files['image']:
                image = request.files['image']
                filename = secure_filename(form.image.data.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.image = form.image.data.filename
            db.session.commit()
            return redirect(request.referrer)
           
        else:
            flash('Redirected to login')
            return redirect("login", 302)
        

#handle update button on admin page
@auth.route("/updateButton/<post_id>", methods=["POST", "GET"])
def updateButton(post_id):
    if 'user_id' in session:
        return redirect(url_for("auth.update_post_view", post_id=post_id))

    else:
        flash('Redirected to login')
        return redirect(url_for("auth.admin"))

#deleting posts
@auth.route("/delete/<post_id>")
def delete(post_id):
    if 'user_id' in session:
        Posts.query.filter_by(_id=post_id).delete()
        db.session.commit()
        #redirect user to admin page after deletion
        return redirect(request.referrer)

    else:
        flash('Redirected to login')
        return redirect(url_for("auth.login"))

#logout
@auth.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash('Logged out')
    return redirect('/posts', 302)
