from .model import db , Admin , Customer , Professional , Package , Booking
from app import app

with app.app_context():
    db.create_all()

    if not db.session.query(Admin).first():
        admin = Admin(email="ad@g.com" , password = "pass")
        db.session.add(admin)
        db.session.commit()
    
    if not db.session.query(Customer).first():
        cust1 = Customer(name="cust1" , email="c1@g.com", password="pass" ,address="Delhi" , mobile ="1234567890")
        cust2= Customer(name="cust2" , email="c2@g.com", password="pass" , address="Mumbai" , mobile ="1234567890")
        db.session.add_all([cust1,cust2])
        db.session.commit()

    if not db.session.query(Professional).first():
        prof1 = Professional(name="prof1" , email="p1@g.com", password="pass" ,address="Delhi" ,status="Active" , mobile ="1234567890" , resume = "hello")
        prof2= Professional(name="prof2" , email="p2@g.com", password="pass" , address="Mumbai" ,status="Active" , mobile ="1234567890" , resume ="hello")
        db.session.add_all([prof1, prof2])
        db.session.commit()
    if not db.session.query(Package).first():
        pack1= Package(title="Pack1" , total_price = "100" , status="Active" , description = "sdjfkadsf" , prof_id=1)
        pack2= Package(title="Pack2" , total_price = "100" , status="Active" , description = "sdjfkadsf" , prof_id=2)
        pack3 =Package(title="Pack3" , total_price = "100" , status="Active" , description = "sdjfkadsf" , prof_id=1)
        db.session.add_all([pack1 , pack2 , pack3])
        db.session.commit()
    
    # prof = db.session.query(Professional).filter_by(id= 2).first()
    

    # print("all packages of the professional 1 : " , prof.packages[0].title )

    # pack = db.session.query(Package).filter_by(id = 2).first()
    # print("prof of this pack is " , pack.prof.email)