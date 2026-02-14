from flask import render_template, request, redirect, session
from config import Config
from app.models.property_model import create_property, get_properties, toggle_property_status, get_matching_properties,get_property_by_id, update_property
from app.models.client_model import create_client, get_all_clients
from app.utils import parse_client_form, parse_property_form

def register_routes(app):

    @app.route("/")
    def dashboard():
        if not session.get("logged_in"):
            return redirect("/login")
        search = request.args.get("search")
        mode = request.args.get("mode")
        
        properties = get_properties(search=search, mode=mode)
        return render_template(
            "dashboard.html", 
            properties=properties,
            search=search,
            mode=mode,
        )

    @app.route("/add-property", methods=["GET", "POST"])
    def add_property():
        if not session.get("logged_in"):
            return redirect("/login")

        if request.method == "POST":
            data = {
                "type": request.form["type"],
                "mode": request.form["mode"],
                "location": request.form["location"],
                "budget": int(request.form["budget"]),
                "area": int(request.form["area"]),
                "owner_name": request.form["owner_name"],
                "owner_contact": request.form["owner_contact"]
            }

            create_property(data)
            return redirect("/")

        return render_template("add_property.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if (request.form["username"] == Config.ADMIN_USERNAME and
                request.form["password"] == Config.ADMIN_PASSWORD):
                session["logged_in"] = True
                return redirect("/")
            return "Invalid credentials"

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.route("/health")
    def health():
        return {"status": "alive"}
    
    @app.route("/toggle-status/<int:property_id>", methods=["POST"])
    def toggle_status(property_id):
        if not session.get("logged_in"):
            return redirect("/login")

        toggle_property_status(property_id)
        return redirect("/")
    
    @app.route("/clients")
    def clients():
        if not session.get("logged_in"):
            return redirect("/login")

        clients = get_all_clients()
        return render_template("clients.html", clients=clients)

    @app.route("/add-client", methods=["GET", "POST"])
    def add_client():
        if not session.get("logged_in"):
            return redirect("/login")

        if request.method == "POST":
            data = parse_client_form(request.form)
            create_client(data)
            return redirect("/clients")
        
        return render_template("add_client.html")

    @app.route("/client/<int:client_id>/matches")
    def client_matches(client_id):
        if not session.get("logged_in"):
            return redirect("/login")

        from app.models.client_model import get_all_clients

        clients = get_all_clients()
        client = next((c for c in clients if c["id"] == client_id), None)

        if not client:
            return "Client not found"

        properties = get_matching_properties(client)

        return render_template(
            "client_matches.html",
            client=client,
            properties=properties
        )

    @app.route("/edit-property/<int:property_id>", methods=["GET", "POST"])
    def edit_property(property_id):
        if not session.get("logged_in"):
            return redirect("/login")

        property = get_property_by_id(property_id)

        if not property:
            return "Property not found"

        if request.method == "POST":
            data = parse_property_form(request.form)
            update_property(property_id, data)
            return redirect("/")

        return render_template("edit_property.html", property=property)

