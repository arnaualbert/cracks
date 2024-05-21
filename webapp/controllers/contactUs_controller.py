from flask import Blueprint, request, render_template, redirect, session
from controllers.login_controller import check_is_logged
from controllers.login_controller import get_connection
import os 
from datetime import datetime

contact_module = Blueprint('contact_module', __name__, template_folder='templates')

def get_current_user():
    return os.getlogin()


def get_current_datetime():
    current_datetime = datetime.now()
    return current_datetime

@contact_module.route("/contact_us", methods=["GET","POST"])
def contactus():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():  
        return render_template("contact_us.html",username=username)
    else:
        return redirect("/login")
    
@contact_module.route("/put_incidents",  methods=["POST"])
def user_incidents():
    username = session.get("username")
    if request.method == "POST" and check_is_logged():
        username = request.form["username"]
        email = request.form["email"]
        type_incident = request.form["type_incident"]
        touched_service = request.form["touched_service"]
        comment = request.form["comment"]

        if "file" in request.files:
            file = request.files["file"]
            if file.filename != '':
                save_data(username, email, type_incident, touched_service, comment, file)
            else:
                save_data(username, email, type_incident, touched_service, comment, None) 
        
        else:
            save_data(username, email, type_incident, touched_service, comment, None) 
        
    
        message = "Incident was sent successfully!"  
        
        return render_template("contact_us.html", message_show=message, username=username)
    
def save_data(username, email, type_incident, touched_service, comment, file):
    current_user = get_current_user()
    print(file)
    date = get_current_datetime()
    directory = f"/home/arnau/Desktop/cracks/incident"

    if not os.path.exists(directory):
        os.makedirs(directory)


    filename = f"{username}_{date}.txt"
    #creamos el fichero
    filepath = os.path.join(directory, filename)

    # Guardar la información en el archivo
    with open(filepath, "w") as f:
        f.write(f"Username: {username}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Type of Incident: {type_incident}\n")
        f.write(f"Touched Service: {touched_service}\n")
        f.write(f"Comment: {comment}\n")

    # Guardamos el archivo adjunto
    if file is not None:
        file.save(os.path.join(directory,file.filename))
    print("all done")