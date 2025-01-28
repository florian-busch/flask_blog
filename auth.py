from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from forms import PostForm, LoginForm, SignupForm
from models import db, Posts, Users
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint("auth", __name__, template_folder="../templates")

# #CRUD
#deleting posts
@auth.route("/delete/<post_id>")
def delete(post_id):
    if 'user_id' in session:
        form = PostForm()
        Posts.query.filter_by(_id=post_id).delete()
        db.session.commit()
        return render_template("admin.html",
                                form=form,
                                message="Post deleted",
                                values=Posts.query.all()
                                )
    else:
        flash('Redirected to login')
        return redirect(url_for("auth.login"))
    
#admin page and save posts to db
@auth.route("/admin", methods=["GET", "POST"])
def post():
    headline = None
    textarea = None
    form = PostForm()
    if request.method=="GET":
        if 'user_id' in session:
            return render_template("admin.html",
                                headline = headline,
                                textarea = textarea,
                                form = form,
                                values=Posts.query.all()
                                )
        else:
            flash('Redirected to login')
            return redirect("login", 302)

                            
    #validate form
    if form.validate_on_submit():
        if 'user_id' in session:
            post = Posts(form.headline.data, form.textarea.data)
            form.headline.data = ""
            form.textarea.data = ""
            db.session.add(post)
            db.session.commit()
            return render_template("admin.html",
                                form = form,
                                message="Post saved",
                                values=Posts.query.all()
                                )
    

#user signup
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method=="GET":
        return render_template("signup.html",
                            form = form,
                            message="User registered",
                            )
    #validate form
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
                return render_template("signup.html",
                                    form = form,
                                    message="User registered",
                                    )
            #db.IntegrityError did not work so changed for exc
            except exc.IntegrityError:
                error = f"User {username} already exists"
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
    # if form.validate_on_submit():
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

#logout
@auth.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    flash('Logged out')
    return redirect('login')
