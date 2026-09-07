from flask import Blueprint, render_template
from music.authentication.authentication import login_required

favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route('/favourites', methods=['GET'])
@login_required
def favourites():
    return render_template("index.html")
