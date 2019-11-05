from flask import Flask,render_template,redirect,request,url_for,session,flash
import os
import shopDB as sd
import itemDB as idb
import werkzeug.contrib.wrappers
import werkzeug.urls

app = Flask(__name__, static_url_path='')
app.secret_key = 'this is a secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    if 'email' in session:
        email = session['email']
        shop = sd.getShop(email)
        return render_template('index.html', shop=shop)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getin', methods=['POST'])
def getin():
    email = request.form.get("email")
    password = request.form.get("password")
    shop = sd.shopLogin(email)
    if(email==shop[0][0] and password==shop[0][1]):
        session['email'] = email
        return redirect(url_for('index'))
    else:
        flash('Wrong \"username\" or \"password\"..\nTry again..')
        return redirect(url_for('login'))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/regShop', methods=["POST"])
def regShop():
    target = APP_ROOT + '/static/images'
    shopname = request.form.get("shopname")
    owner = request.form.get("owner")
    email = request.form.get("email")
    address = request.form.get("address")
    password = request.form.get("password")
    imgfile = request.files.get("img")

    if(imgfile):
        img = imgfile.filename
        destination = "/".join([target,img])
        imgfile.save(destination)
    else:
        img = 'default.png'

    sd.createShop(shopname,owner,email,address,password,img)
    return redirect(url_for('login'))

@app.route("/updateDetails", methods=["POST"])
def updateDetails():
    if 'email' in session:
        target = APP_ROOT + '/static/images'
        shopname = request.form.get("shopname")
        owner = request.form.get("owner")
        email = session['email']
        address = request.form.get("address")
        password = request.form.get("password")
        imgfile = request.files.get("img")
        password2 = sd.getPassword(email)

        if(imgfile):
            img = imgfile.filename
            destination = "/".join([target,img])
            imgfile.save(destination)
        else:
            img = sd.getImage(email)

        sd.updateInfo(shopname,owner,email,address,password,img)

        if(password == password2):
            return redirect(url_for('index'))
        else:
            flash("Changed \"Password\".. \nLogin again with \"Updated Password\"..")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/items')
def items():
    if 'email' in session:
        item = idb.getItems(session['email'])
        return render_template('items.html',item=item)
    else:
        return redirect(url_for('login'))

@app.route('/item/<int:pid>')
def item(pid):
    if 'email' in session:
        pitem = idb.getItem(session['email'],pid)
        if(len(pitem)):
            return render_template('item.html',pitem=pitem)
        else:
            return render_template('notfound.html')
    else:
        return redirect(url_for('login'))

@app.route('/item/<int:pid>/update')
def update(pid):
    if 'email' in session:
        item = idb.getItem(session['email'],pid)
        return render_template('updateitem.html',item=item)
    else:
        return redirect(url_for('login'))

@app.route('/item/<int:pid>/updateItem', methods=["POST"])
def updateItem(pid):
    if 'email' in session:
        target = APP_ROOT + '/static/images/productImages'
        email = session['email']
        itemname = request.form.get("itemname")
        itemdesc = request.form.get("itemdesc")
        units = request.form.get("units")
        mrp = request.form.get("mrp")
        awaycost = request.form.get("awaycost")
        awaypktcost = request.form.get("awaypktcost")
        localcost = request.form.get("localcost")
        localpktcost = request.form.get("localpktcost")
        date = request.form.get("date")
        imgfile = request.files.get("img")

        if(imgfile):
            img = imgfile.filename
            destination = "/".join([target,img])
            imgfile.save(destination)
        else:
            img = idb.getImage(pid)
        
        idb.updateItem(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img,pid)

        return redirect(url_for('item',pid=pid))
    else:
        return redirect(url_for('login'))

@app.route('/additems')
def additems():
    if 'email' in session:
        return render_template('additem.html')
    else:
        return redirect(url_for('login'))

@app.route('/additem', methods=["POST"])
def additem():
    if 'email' in session:
        target = APP_ROOT + '/static/images/productImages'
        email = session['email']
        itemname = request.form.get("itemname")
        itemdesc = request.form.get("itemdesc")
        units = request.form.get("units")
        mrp = request.form.get("mrp")
        awaycost = request.form.get("awaycost")
        awaypktcost = request.form.get("awaypktcost")
        localcost = request.form.get("localcost")
        localpktcost = request.form.get("localpktcost")
        date = request.form.get("date")
        imgfile = request.files.get("img")

        if(imgfile):
            img = imgfile.filename
            destination = "/".join([target,img])
            imgfile.save(destination)
        else:
            img = 'defaultItem.png'
        
        idb.enterItem(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img)
        flash("New Item Successfully Added !")

        return redirect(url_for('items'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5003, debug=True)