from app  import app
from .model import db  , Admin, Customer,Professional,Package,Booking

from flask_login import login_user , login_required , current_user

from flask import render_template , request ,redirect 

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
        
            new_user= Professional(name=name , email=email , password=password , mobile=mobile , address=address , status="Registered" , resume="default_resume.pdf")
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
        if  isinstance(user,Professional):
            if user.password == password:
                login_user(user)
                return redirect(f"/professional/dashboard")
        elif isinstance(user,Customer):
            if user.password == password:
                login_user(user)
                return redirect(f"/customer/dashboard")
        elif isinstance(user,Admin):
            if user.password == password:
                login_user(user)
                return redirect("/admin/dashboard") 




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
    return f"welcome {current_user.email} to customer dashbaord" 


@app.route("/professional/dashboard" , methods=["GET","POST"]) 
@login_required
def professional_dashboard():
    
    return render_template("professional/dashboard.html" , current_user=current_user)


@app.route("/professional/search" , methods=["GET" ,"POST"]) 
@login_required
def prof_search():
    return render_template("professional/search.html")


@app.route("/view-professional/<int:id>" , methods=["GET" , "POST"])
@login_required
def view_professional(id):
    prof = db.session.query(Professional).filter_by(id = id).first()
    packages = prof.packages
    return render_template( "/admin/view-professional.html" , prof = prof , packages = packages)




