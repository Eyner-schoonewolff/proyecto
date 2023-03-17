from flask import Blueprint, render_template, redirect, url_for, request, session

menus = Blueprint('menus', __name__, static_url_path='/static',
                  template_folder="templates");



@menus.route("/solicitar")
def solicitar():

    return render_template("solicitar.html")


@menus.route("/inicio")
def inicio():

    return render_template("home.html")