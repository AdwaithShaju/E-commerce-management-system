from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user



local_server= True
app = Flask(__name__)
app.secret_key='harshithbhaskar'



login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/sellers'
db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class Category(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    categorytype=db.Column(db.String(100))


class Products(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    sellername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.String(50))
    address=db.Column(db.String(50))
    products=db.Column(db.String(50))

    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/sellerdetails')
@login_required
def sellerdetails():

    query=Register.query.all()
    return render_template('sellerdetails.html',query=query)

@app.route('/agroproducts')
def agroproducts():
  
    query=Products.query.all()
    return render_template('products.html',query=query)

@app.route('/product',methods=['POST','GET'])
@login_required
def product():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=Products(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addproducts.html')

@app.route('/triggers')
@login_required
def triggers():
  
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/addproducts',methods=['POST','GET'])
@login_required
def addproducts():
    if request.method=="POST":
        categorytype=request.form.get('products')
        query=Category.query.filter_by(categorytype=categorytype).first()
        if query:
            flash("Category Type Already Exist","warning")
            return redirect('/addproducts')
        dep=Category(categorytype=categorytype)
        db.session.add(dep)
        db.session.commit()
        flash("Category Addes","success")
    return render_template('type.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
  
    post=Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/sellerdetails')


@app.route("/edit/<string:rid>",methods=['POST','GET'])
@login_required
def edit(rid):

    if request.method=="POST":
        sellername=request.form.get('sellername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        categorytype=request.form.get('categorytype')     
        
        post=Register.query.filter_by(rid=rid).first()
        print(post.sellername)
        post.sellername=sellername
        post.adharnumber=adharnumber
        post.age=age
        post.gender=gender
        post.phonenumber=phonenumber
        post.address=address
        post.products=categorytype
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/sellerdetails')
    posts=Register.query.filter_by(rid=rid).first()
    products=Category.query.all()
    return render_template('edit.html',posts=posts,products=products)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

      
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/register',methods=['POST','GET'])
@login_required
def register():
    products=Category.query.all()
    if request.method=="POST":
        sellername=request.form.get('sellername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        categorytype=request.form.get('categorytype')     
        query=Register(sellername=sellername,adharnumber=adharnumber,age=age,gender=gender,phonenumber=phonenumber,address=address,products=categorytype)
        db.session.add(query)
        db.session.commit()
       
        return redirect('/sellerdetails')
    return render_template('seller.html',products=products)

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    
