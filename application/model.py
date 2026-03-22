from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class Admin(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String , unique= True , nullable =False)
    password = db.Column(db.String , nullable = False)

     
    def get_id(self):
        return self.email

class Customer(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String , unique= True , nullable =False)
    password = db.Column(db.String , nullable = False)
    name = db.Column(db.String , nullable = False)
    address = db.Column(db.String , nullable = False)
    mobile = db.Column(db.String , nullable = False)
    status= db.Column(db.String )
    created_bookings = db.relationship("Booking" , backref="cust")

    def get_id(self):
        return self.email


class Professional(db.Model , UserMixin):
    __tablename__="professional"
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String , unique= True , nullable =False)
    password = db.Column(db.String , nullable = False)
    name = db.Column(db.String , nullable = False)
    address = db.Column(db.String , nullable = True)
    mobile = db.Column(db.String , nullable = True)
    resume  =db.Column(db.String , nullable = False)
    status = db.Column(db.String , nullable = False)
    packages = db.relationship("Package" , backref="prof" )
    recived_bookings= db.relationship("Booking" , backref= "prof")

    def get_id(self):
        return self.email

    


class Package(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    
    title = db.Column(db.String , nullable = False)
    total_price = db.Column(db.String , nullable = True)
    description = db.Column(db.String , nullable = False)
    status= db.Column(db.String , nullable = False)
    prof_id = db.Column(db.Integer , db.ForeignKey("professional.id") , nullable = False )
    associated_bookings = db.relationship("Booking" , backref="pack")


class Booking(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    date= db.Column(db.Date , nullable =False)
    start_time = db.Column(db.Time , nullable = False)
    end_time = db.Column(db.Time )
    status = db.Column(db.String , nullable = False)
    package_id  = db.Column(db.Integer , db.ForeignKey("package.id") , nullable = False )
    customer_id = db.Column(db.Integer , db.ForeignKey("customer.id") , nullable = False )
    professional = db.Column(db.Integer , db.ForeignKey("professional.id") , nullable = False )



