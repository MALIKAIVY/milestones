# Create an empty server
# then run while debug is True:

# import pmysql- helps you connect to python mysql database
from flask import*
import pymysql
def db_connection():
    return pymysql.connect(host='localhost', user='root', password='', database='soko_garden_db')

app=Flask(__name__)
app.secret_key = "awrfgnfgfgtnhbnvm"
@app.route('/')
def home():
    # connected to the database
    connection = db_connection()

    # fashion
    sql_fashion = "select * from products where product_category = 'Fashion'"
    cursor_fashion = connection.cursor()
    cursor_fashion.execute(sql_fashion)
    fashion = cursor_fashion.fetchall()

    # electronics
    sql_electronics = "select * from products where product_category = 'Electronics'"
    cursor_electronics = connection.cursor()
    cursor_electronics.execute(sql_electronics)
    electronics = cursor_electronics.fetchall()

    # shirts
    sql_shirts = "select * from products where product_category = 'Shirts'"
    cursor_shirts = connection.cursor()
    cursor_shirts.execute(sql_shirts)
    shirts = cursor_shirts.fetchall()

    # shoes
    sql_shoes = "select * from products where product_category = 'Shoes'"
    cursor_shoes = connection.cursor()
    cursor_shoes.execute(sql_shoes)
    shoes = cursor_shoes.fetchall()

    # watches
    sql_watches = "select * from products where product_category = 'Trousers'"
    cursor_watches = connection.cursor()
    cursor_watches.execute(sql_watches)
    watches = cursor_watches.fetchall()


    return render_template('home.html', fashion = fashion, electronics=electronics, shirts = shirts, shoes=shoes, watches = watches)
# create a route:
# login

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = db_connection()
        cursor = connection.cursor()

        sql = "select * from users where email =%s and password =%s"
        data = (email, password )
        cursor.execute(sql, data)

        # check whether username is avalable or not
        count = cursor.rowcount
        if count ==0:
            return render_template('login.html', message1 = 'Invalid Credentials')
        else:
            user = cursor.fetchone()
            session['key'] = user[1]
            return redirect('/')

    else:
        return render_template('login.html', message2 = 'Login Here' )

@app.route('/register', methods=['POST', 'GET'])
def register():
    # step1: Check wether its POST or GET 
    if request.method == 'POST':
        # step2: request data
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password= request.form['password']
        confirm = request.form['confirm']

        # Database Connection
        connection=db_connection()
        # cursor(): give connection ability to run sql
        cursor = connection.cursor()
        sql = "insert into users (username, email, phone, password) values(%s, %s, %s, %s)"

        data = (username, email, phone, password)
        # password checks
        if password !=confirm:
            return render_template('register.html', message= 'password dont match!')
        
        elif len(password) < 8:
            return render_template('register.html', message = 'password less than 8 characters!')
        
        else:
            cursor.execute(sql,data)
            connection.commit()
            return render_template('register.html',success ='register successful')
    else:
        return render_template('register.html', message = 'Register Here')
    
    # 4. Product Upload
@app.route('/upload', methods = ['POST', 'GET'] )
def upload():
    if request.method == 'POST':
        # capture data from form: name
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_discount = request.form['product_discount']
        product_category = request.form['product_category']
        # files in your computer
        product_image1 = request.files['product_image1']
        product_image2 = request.files['product_image2']
        product_image3 = request.files['product_image3']

        # save the three images in your application
        # static/images/
        product_image1.save('static/images/' + product_image1.filename)
        product_image2.save('static/images/' + product_image2.filename)
        product_image3.save('static/images/' + product_image3.filename)

        # Database Connection and Cursor()
        connection = db_connection()
        cursor = connection.cursor()

        # sql: to insert a product record
        sql = "insert into products (product_name, product_desc, product_cost, product_discount, product_category, product_image1, product_image2, product_image3) values (%s, %s, %s, %s, %s, %s, %s, %s)"

        data = (product_name, product_desc, product_cost, product_discount, product_category, product_image1.filename, product_image2.filename, product_image3.filename)

        cursor.execute(sql, data)
        connection.commit()
        return render_template('upload.html', message1 = 'Product Added Successfully')


    else:
        return render_template('upload.html', message2 = "Please Add the Product")
    
    # Single Page
# Route Parameters(<>): Store values on a route components
@app.route('/single/<product_id>')
def single(product_id):
    connection = db_connection()
    cursor_single = connection.cursor()

    sql = "select * from products where product_id = %s"
    cursor_single.execute(sql, product_id)

    single_record = cursor_single.fetchone()
    return render_template('single.html', single_record = single_record)

# Dispalying All Products from one category

# 1. Fashion
@app.route('/fashion')
def fashion():
    connection = db_connection()
    cursor_fashion = connection.cursor()

    sql_fashion = "select * from products where product_category = 'Fashion' order by rand() limit 8"
    cursor_fashion.execute(sql_fashion)

    fashion = cursor_fashion.fetchall()
    
    return render_template('fashion.html', fashion = fashion)


# 2. Shoes
@app.route('/shoes')
def shoes():
    connection = db_connection()
    cursor_shoes = connection.cursor()

    sql_shoes = "select * from products where product_category = 'Shoes' order by rand() limit 8"
    cursor_shoes.execute(sql_shoes)

    shoes = cursor_shoes.fetchall()

    return render_template('shoes.html', shoes = shoes)

@app.route('/mpesa', methods = ['POST', 'GET'])
def payment():
    phone = str(request.form['phone'])
    amount = str(request.form['amount'])

    from mpesa import stk_push
    stk_push(phone, amount)

    return "Please Check Your Phone to Complete Payment"

@app.route('/send_reviews', methods= ['POST', 'GET'])
def send_reviews():
    connection = db_connection()
    cursor_reviews = connection.cursor()

    # request data
    message = request.form['message']
    name = request.form['name']
    email = request.form['email']

    sql = "insert into reviews(review_message, client_name, client_email) values(%s, %s, %s)"
    data = (message, name, email)

    cursor_reviews.execute(sql, data)
    connection.commit()
    return render_template('reviews.html', message = 'Review Sent')




app.run(debug=True)
