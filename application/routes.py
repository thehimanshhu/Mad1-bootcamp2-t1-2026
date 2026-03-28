from app  import app
from .model import db  , Admin, Customer,Professional,Package,Booking
from datetime import datetime
from flask_login import login_user , login_required , current_user ,logout_user

from flask import render_template , request ,redirect ,flash

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register/<string:utype>" , methods=["GET" , "POST"])
def register(utype):
    if request.method =="GET":
        if utype == "professional":
            return render_template("professional/register.html")
        elif utype=="customer":
            return render_template("customer/register.html")
        else:
            return "not a valid url"
    elif request.method =="POST":
        if utype=="customer":
            email = request.form.get("cust_email")
            password= request.form.get("cust_password")
            name = request.form.get("cust_name")
            mobile = request.form.get("cust_mobile")
            address = request.form.get("cust_address")
            if not email or not password or not name or not mobile or not address :
                return "please fill the form properly"
            
            user = db.session.query(Professional).filter_by(email=email).first() or \
                 db.session.query(Customer).filter_by(email=email).first() or\
                 db.session.query(Admin).filter_by(email=email).first()
            if user:
                return '''
                        <h1>User already exist</h1>
                        <a href="/login" >Go to login </a>
                        '''
        
            new_user= Customer(name=name , email=email , password=password , mobile=mobile , address=address)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")

        if utype=="professional":
            email = request.form.get("prof_email")
            password= request.form.get("prof_password")
            name = request.form.get("prof_name")
            mobile = request.form.get("prof_mobile")
            address = request.form.get("prof_address")
            resume = request.files.get("prof_resume")
            
            if not email or not password or not name or not mobile or not address :
                return "please fill the form properly"
            
            user = db.session.query(Professional).filter_by(email=email).first() or \
                 db.session.query(Customer).filter_by(email=email).first() or\
                 db.session.query(Admin).filter_by(email=email).first()
            if user:
                return '''
                        <h1>User already exist</h1>
                        <a href="/login" >Go to login </a>
                        '''
            resume.save(f"./static/{email}.pdf")
            new_user= Professional(name=name ,resume= f"/static/{email}.pdf" , email=email , password=password , mobile=mobile , address=address , status="Registered")
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")


@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")
    elif request.method =="POST":
        email=request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(Professional).filter_by(email=email).first() or \
                 db.session.query(Customer).filter_by(email=email).first() or\
                 db.session.query(Admin).filter_by(email=email).first()
        if not user:
            return "email doesn't exist"
        if  isinstance(user,Professional):
            if user.password == password:
                if user.status=="Registered":
                    flash("Your application is pending for admins approval . please wait")
                    return redirect("/login")
                elif user.status=="Flagged":
                    return "You have been flagged by admin. please contact admin"
                login_user(user)
                return redirect(f"/professional/dashboard")
            else:
                return "Check password"
            
        elif isinstance(user,Customer):
            if user.password == password:
                login_user(user)
                return redirect(f"/customer/dashboard")
            else: 
                return "check password"
        elif isinstance(user,Admin):
            if user.password == password:
                login_user(user)
                return redirect("/admin/dashboard") 
            else:
                return "check password"




# @app.route("/login", methods=["GET" , "POST"])
# def login():
#     if request.method =="GET":
#         return render_template("login.html")
#     elif request.method =="POST":
#         email=request.form.get("email")
#         password = request.form.get("password")
#         role = request.form.get("role")

#         if role=="admin":
#             adm = db.session.query(Admin).filter_by(email=email).first()
#             if adm :
#                 if adm.password==password :
#                     return redirect("/admin/dashboard")
#                 else:
#                     return "invalid password"
#             else:
#                 return ("user not found")
#         elif role=="prof":
#             prof = db.session.query(Professional).filter_by(email=email).first()
#             if adm :
#                 if adm.password==password :
#                     return redirect("/professional/dashboard")
#                 else:
#                     return "invalid password"
#             else:
#                 return ("user not found")



@app.route("/admin/dashboard" , methods=["GET","POST"]) 
@login_required
def admin_dashboard():

    profs = db.session.query(Professional).all()
    custs=db.session.query(Customer).all()
    return render_template("admin/dashboard.html" , professionals=profs , customers=custs)


@app.route("/customer/dashboard" , methods=["GET","POST"]) 
@login_required
def customer_dashboard():
    profs = db.session.query(Professional).filter_by(status="Active").all()
    return render_template("/customer/dashboard.html" , professionals=profs , current_user = current_user)


@app.route("/professional/dashboard" , methods=["GET","POST"]) 
@login_required
def professional_dashboard():
    packs  = current_user.packages
    return render_template("professional/dashboard.html" , current_user=current_user , packs= packs)


@app.route("/professional/search" , methods=["GET" ,"POST"]) 
@login_required
def prof_search():
    return render_template("professional/search.html")


@app.route("/view-professional/<int:id>" , methods=["GET" , "POST"])
@login_required
def view_professional(id):
    
    prof = db.session.query(Professional).filter_by(id = id).first()
    packages = prof.packages
    if isinstance(current_user, Admin):
        return render_template( "/admin/view-professional.html" , prof = prof , packages = packages)
    elif isinstance(current_user , Customer):
        return render_template("/customer/view-professional.html" , prof=prof , packages = packages)
    

@app.route("/book/<int:packid>" , methods=["GET" , "POST"])
@login_required
def book_package(packid):
    if request.method=="GET" : 
        # existing_booking = db.session.query(Booking).filter(Booking.customer_id == current_user.id , Booking.package_id == packid).first()
        # if existing_booking : 
        #     return "already booked"
        return render_template("customer/booking.html" , id = packid)
    elif request.method=="POST":
        print(type(request.form.get("book_date")))
        d = datetime.strptime(request.form.get("book_date") , "%Y-%m-%d").date()
        
        t = datetime.strptime(request.form.get("book_time") , "%H:%M").time()
        
        package = db.session.query(Package).filter_by(id = packid).first()
        book = Booking(date = d , start_time = t , status = "Pending" , package_id = packid , customer_id = current_user.id , professional= package.prof_id)
        db.session.add(book)
        db.session.commit()
        return redirect("/customer/dashboard")
    

@app.route("/view-customer/<int:id>" , methods=["GET" , "POST"])
@login_required
def view_customer(id):
    cust = db.session.query(Customer).filter_by(id = id).first()
    # packages = prof.packages
    bookings = cust.created_bookings
    return render_template( "/admin/view-customer.html" , cust= cust , bookings = bookings)


@app.route("/admin/professional/<string:action>/<int:id>" )
def admin_action_on_professional(action , id):
    prof = db.session.query(Professional ).filter_by(id = id).first()
    if action=="active" and prof.status =="Registered"  :
        prof.status = "Active"
        db.session.commit()
    elif action == "reject" and prof.status=="Registered" :
        prof.status = "Rejected"
        db.session.commit()
    elif action == "flag" and prof.status=="Active":
        prof.status = "Flagged"
        db.session.commit()
    elif action == "unflag" and prof.status=="Flagged":
        prof.status = "Active"
        db.session.commit()
    else : 
        return "Wrong action"

    return redirect("/admin/dashboard")



@app.route("/admin/customer/<string:action>/<int:id>" )
def admin_action_on_customer(action , id):
    cust = db.session.query(Customer ).filter_by(id = id).first()
   
    if action == "flag" and cust.status=="Active":
        cust.status = "Flagged"
        db.session.commit()
    elif action == "unflag" and cust.status=="Flagged":
        cust.status = "Active"
        db.session.commit()
    else : 
        return "Wrong action"

    return redirect("/admin/dashboard")

@app.route("/professional/create-package" , methods=["GET" , "POST"])
def create_package():
    if request.method=="GET":
        return render_template("professional/create-package.html")
    elif request.method=="POST":
        name = request.form.get("pack_name")
        desc = request.form.get("pack_desc")
        price = request.form.get("pack_price")

        new_pack = Package(title = name , description=desc , total_price = price , status= "Pending" , prof_id =current_user.id)
        db.session.add(new_pack)
        db.session.commit()
        return redirect("/professional/dashboard")
    
@app.route("/professional/edit-package/<int:id>" , methods=["GET" , "POST"])
def edit_package(id):
    if request.method=="GET":
        pack = db.session.query(Package).filter_by(id = id).first()
        return render_template("professional/edit-package.html" , pack=pack)
    elif request.method=="POST":
        name = request.form.get("pack_name")
        desc = request.form.get("pack_desc")
        price = request.form.get("pack_price")

        pack = db.session.query(Package).filter_by(id = id).first()
        if name :
            pack.title = name
        if desc:
            pack.description=desc
        if price:
            pack.total_price = price

        db.session.commit()
        return redirect("/professional/dashboard")
    
@app.route("/admin/package/<string:action>/<int:id>")
def admin_action_on_package(action,id):
    pack = db.session.query(Package).filter_by(id = id).first()
    if action=="approve" and pack.status =="Pending":
        pack.status="Approved"
    elif action =="reject" and pack.status=="Pending":
        pack.status ="Rejected"
    db.session.commit()
    return redirect("/admin/dashboard")


@app.route("/package-details/<int:id>" , methods= ["GET" , "POST"])
def package_details(id):
    pack = db.session.query(Package).filter_by(id = id).first()
    if isinstance(current_user,Admin):
        return render_template("admin/package-details.html", pack=pack)
    elif isinstance(current_user , Professional):
        
        return render_template("professional/package-details.html" , pack=pack , current_user=current_user)
    return "Access Denied"


@app.route("/professional/booking/<string:action>/<int:id>")
def professional_action_on_booking(action , id):
    booking = db.session.query(Booking).filter_by(id = id).first()
    if action=="approve" and booking.status =="Pending":
        booking.status="Approved"
    elif action =="reject" and booking.status=="Pending":
        booking.status ="Rejected"
    elif action =="complete" and booking.status=="Approved":
        booking.end_time = datetime.now().time()
        booking.status="Completed"
    db.session.commit()
    return redirect("/professional/dashboard")


@app.route("/admin/search" , methods=["GET" , "POST"])
def admin_search():
    if request.method=="GET": 
        return render_template("admin/search.html")
    elif request.method=="POST":
        search_query = request.form.get("search_query")
        query_type = request.form.get("query_type")
        if query_type =="professional":
            profs = db.session.query(Professional).filter(Professional.name.contains(search_query)).all()
            
            return render_template("admin/search.html" , professionals= profs , qt = query_type )
        elif query_type =="customer":
            custs = db.session.query(Customer).filter(Customer.name.contains(search_query)).all()
            
            return render_template("admin/search.html" , customers= custs , qt = query_type )
        else:
            return "Wrong query type"
        


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")