from flask import render_template, request, redirect, session
from config import Config
from app.models.property_model import create_property, get_properties, toggle_property_status, get_matching_properties,get_property_by_id, update_property, soft_delete_property, restore_property_by_id
from app.models.client_model import create_client, get_all_clients, get_followups_today, get_client_by_id, update_client, get_matching_buyers_for_seller, soft_delete_client, get_clients_filtered
from app.utils import parse_client_form, parse_property_form, parse_broker_property_form
from app.services.request_utils import extract_filters, extract_client_filters, extract_property_filters
from app.services.dashboard_service import build_dashboard_context
from app.services.request_utils import extract_broker_filters
from app.models.broker_property_model import get_broker_properties_filtered, get_broker_properties, get_broker_property_by_id
from app.services.broker_property_service import add_broker_property, get_broker_property_by_id
from app.services.broker_visuals import decorate_broker_properties
from app.models.broker_property_model import update_broker_property
from app.settings.constants import BROKER_PROPERTY_TAGS, AREA_CLUSTERS, CONFIGURATIONS
from datetime import date

def register_routes(app):

    @app.route("/")
    def dashboard():
        if not session.get("logged_in"):
            return redirect("/login")

        dashboard_data = build_dashboard_context()

        return render_template(
            "dashboard.html",
            **dashboard_data
        )
    
    @app.route("/clients/followups")
    def clients_followups():
        if not session.get("logged_in"):
            return redirect("/login")

        followups = get_followups_today()

        return render_template(
            "clients.html",
            clients=followups,
            page_title="Followups Today"
        )
    
    @app.route("/properties")
    def properties():
        if not session.get("logged_in"):
            return redirect("/login")

        filters = extract_property_filters(request)
        properties = get_properties(**filters)

        return render_template(
            "properties.html",
            properties=properties,
            **filters
        )

    @app.route("/property/<int:property_id>")
    def property_detail(property_id):
        if not session.get("logged_in"):
            return redirect("/login")

        property = get_property_by_id(property_id)

        if not property:
            return "Property not found", 404

        return render_template("property_detail.html", property=property)

    @app.route("/add-property", methods=["GET", "POST"])
    def add_property():
        if not session.get("logged_in"):
            return redirect("/login")

        if request.method == "POST":
            data = parse_property_form(request.form)
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

        filters = extract_client_filters(request)
        clients = get_clients_filtered(**filters)

        return render_template("clients.html", 
                               clients=clients,
                               **filters)

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
    
    @app.route("/edit-client/<int:client_id>", methods=["GET", "POST"])
    def edit_client(client_id):
        if not session.get("logged_in"):
            return redirect("/login")

        client = get_client_by_id(client_id)

        if not client:
            return "Client not found"

        if request.method == "POST":
            data = parse_client_form(request.form)
            print("Data to update client...",data)
            update_client(client_id, data)
            return redirect("/clients")

        return render_template("edit_client.html", client=client)

    @app.route("/client/<int:client_id>/buyer-matches")
    def show_buyer_matches(client_id):
        if not session.get("logged_in"):
            return redirect("/login")

        seller = get_client_by_id(client_id)

        if seller["requirement"] != "Sell":
            return redirect("/clients")

        buyers = get_matching_buyers_for_seller(seller)

        return render_template(
            "buyer_matches.html",
            seller=seller,
            buyers=buyers
        )
    
    @app.route("/client/<int:client_id>/delete", methods=["POST"])
    def delete_client(client_id):
        if not session.get("logged_in"):
            return redirect("/login")

        soft_delete_client(client_id)
        return redirect("/clients")
    
    @app.route("/property/<int:property_id>/delete", methods=["POST"])
    def delete_property(property_id):
        if not session.get("logged_in"):
            return redirect("/login")

        soft_delete_property(property_id)
        return redirect("/")
    
    @app.route("/property/<int:property_id>/restore", methods=["POST"])
    def restore_property(property_id):
        if not session.get("logged_in"):
            return redirect("/login")
        
        restore_property_by_id(property_id)
        return redirect("/")
    
    @app.route("/broker-properties")
    def broker_properties():
        if not session.get("logged_in"):
            return redirect("/login")

        filters = extract_broker_filters(request)
        broker_properties = get_broker_properties_filtered(**filters)
        # broker_properties = get_broker_properties()
        broker_properties = decorate_broker_properties(broker_properties)

        print("FILTERS:", filters)
        print("RESULT COUNT:", len(broker_properties))

        return render_template(
            "broker_properties.html",
            properties=broker_properties,
            all_area_clusters = AREA_CLUSTERS,
            all_tags=BROKER_PROPERTY_TAGS,
            all_configurations=CONFIGURATIONS,
            **filters
        )

    @app.route("/broker-property/<int:property_id>/confirm", methods=["POST"])
    def confirm_broker_property_route(property_id):

        if not session.get("logged_in"):
            return redirect("/login")

        from app.services.broker_property_service import confirm_broker_listing

        confirm_broker_listing(property_id)

        return redirect(request.referrer or "/broker-properties")

    @app.route("/broker-property/<int:property_id>/toggle-availability", methods=["POST"])
    def toggle_broker_availability_route(property_id):

        if not session.get("logged_in"):
            return redirect("/login")

        from app.services.broker_property_service import toggle_broker_listing

        toggle_broker_listing(property_id)

        return redirect(request.referrer or "/broker-properties")
    
    @app.route("/add-broker-property", methods=["GET", "POST"])
    def add_broker_property_route():

        if not session.get("logged_in"):
            return redirect("/login")

        if request.method == "POST":

            data = parse_broker_property_form(request.form)
            add_broker_property(data)

            return redirect("/broker-properties")

        return render_template(
            "add_broker_property.html",
            today=date.today().isoformat(),
            tags = BROKER_PROPERTY_TAGS,
            all_area_clusters = AREA_CLUSTERS,
            all_configurations=CONFIGURATIONS
            )
    
    @app.route("/edit-broker-property/<int:property_id>", methods=["GET", "POST"])
    def edit_broker_property(property_id):

        if not session.get("logged_in"):
            return redirect("/login")

        property = get_broker_property_by_id(property_id)

        if not property:
            return "Broker Property not found"

        if request.method == "POST":
            data = parse_broker_property_form(request.form)
            update_broker_property(property_id, data)
            return redirect("/broker-properties")

        return render_template(
            "edit_broker_property.html",
            today=date.today().isoformat(),
            property=property,
            tags=BROKER_PROPERTY_TAGS,
            all_area_clusters = AREA_CLUSTERS,
            all_configurations=CONFIGURATIONS
        )

    @app.route("/broker-property/<int:property_id>")
    def broker_property_detail(property_id):
        if not session.get("logged_in"):
            return redirect("/login")

        property = get_broker_property_by_id(property_id)

        if not property:
            return "Property not found", 404

        return render_template("broker_property_detail.html", property=property)

