from flask import Blueprint, render_template
from models import Posts

main = Blueprint("main", __name__, template_folder="../templates")

@main.route("/", methods=["GET"])
def get_posts():
    try:
        return render_template("posts.html", values=Posts.query.all())
    except:
        return "Error retrieving Posts"
    
@main.route("/about", methods=["GET"])
def about():
    try:
        return render_template("about.html")
    except:
        return "Error retrieving About-Site"

@main.route("/pictures", methods=["GET"])
def pictures():
    try:
        return render_template("pictures.html")
    except:
        return "Error retrieving About-Site"

@main.route("/impressum", methods=["GET"])
def impressum():
    try:
        return render_template("impressum.html")
    except:
        return "Error retrieving About-Site"


#To Do: Errorhandling