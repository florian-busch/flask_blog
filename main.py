from flask import Blueprint, render_template
from models import Posts

main = Blueprint("main", __name__, template_folder="../templates")

@main.route("/", methods=["GET"])
@main.route("/posts", methods=["GET"])

def get_posts():
    try:
        return render_template("posts_overview.html",
                               #works with values, not with posts, not sure why
                                values=Posts.query.all()
                                )
    except:
        return "Error retrieving Posts"
    
@main.route("/about", methods=["GET"])
def about():
    try:
        return render_template("about.html")
    except:
        return "Error retrieving About-Site"

@main.route("/impressum", methods=["GET"])
def impressum():
    try:
        return render_template("impressum.html")
    except:
        return "Error retrieving About-Site"


#To Do: Errorhandling