from extensions import *
from func import *



app = Flask(__name__)

app.config['SECRET_KEY'] = '3af076d4affdded6d0ba9d0f09338a4379ce0324abfe5dc12c7e50461902b008628a87045aa5c2c6ae8065d0bbcff88016c37e86e9eb97d16a67b73c26ce9046'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'



db = SQLAlchemy(app)
arr = []
qty = 0
subtotal = 0
attempts = 0
total = 0



#database here ##########################################################
class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))    
    timestamp = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    #test account if admin
    def is_admin(self, id):
        if id == 1:
            return True
        return False

    def __repr__(self):
        return f'{self.username}'

    def change_password(self, new_pwd):
        self.password = generate_password_hash(new_pwd)



class Profit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, amount):
        self. amount = amount

    def __repr__(self):
        return f'{self.amount}'

    def __add__(self, other):
        self.amount + other

    def __sub__(self, other):
        self.amount - other

    def __mul__(self, other):
        self.amount * other

    def __truediv__(self, other):
        self.amount / other

    def reset(self):
        self.amount = 0

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    expense_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, expense_amount):
        self. expense_amount = expense_amount

    def __repr__(self):
        return f'{self.expense_amount}'

    def __add__(self, other):
        self.expense_amount + other

    def __sub__(self, other):
        self. expense_amount - other

    def __mul__(self, other):
        self.expense_amount * other

    def __truediv__(self,other):
        self.expense_amount / other

    def reset(self):
        self.expense_amount = 0



class Sales(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sales_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, sales_amount):
        self. sales_amount = sales_amount

    def __repr__(self):
        return f'{self.sales_amount}'

    def __add__(self, other):
        self.sales_amount + other

    def __sub__(self, other):
        self.sales_amount - other

    def reset(self):
        self.sales_amount = 0


# categories = db.Table(
#     'categories',
#     db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
# )


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.relationship('Category', backref = 'stock', lazy=True)
    unit_price = db.Column(db.Float)
    received_quantity = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default= datetime.now())


    def check_available_stock(self):
        return self.session.query(self.model).filter(self.model.quantity >=0)

    def add_stock(self, qty):
        self.quantity + qty
        db.session.add(self.quantity)
        db.session.commit()

    def update_stock(self, qty):
        quant = Stock.query.get(quantity)
        db.session.commit()

    def check_stock(self):
        if self.quantity < 1:
            self.is_out_of_stock = True
        self.is_out_of_stock =  False



class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    types = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    comment = db.Column(db.Text)
    stocks = db.Column(db.Integer, db.ForeignKey('stock.id'))
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __init__(self, name, types, brand, quantity,comment):
        self.name = name
        self.types = types
        self.brand = brand
        self.quantiy = quantity
        self.comment = comment

    def identifier(self):
        return self.name
    
    def __repr__(self):
        return f'{self.id}'

    def pos_name(self):
        return f'{self.id}{self.brand} {self.name} {self.types}'


class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __str__(self):
        return self.name

    def __init__(self, name, category):
        self.name = name
        self.category = category


class BrandName(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name

#the TYPE class
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     category_id= db.relationship('Category', secondary=categories, backref = 'category', lazy = True, uselist = False)
#     product_type = db.Column(db.String(255))
#     brand = db.Column(db.String(255))
#     quantity = db.Column(db.Integer) # per box
#     comment = db.Column(db.Text)
#     name = db.Column(db.String(255))
#     unit_price = db.Column(db.Float)
#     stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
#     timestamp = db.Column(db.DateTime, default= datetime.now())
    
    # purchases = db.relationship('Purchase', backref='product', lazy = 'dynamic')
    # products = db.Column(db.Integer, db.ForeignKey('category.id'))
   
    # def __repr__(self):
    #     return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True)
    username = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    middle_initial = db.Column(db.String(20))
    password = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default = datetime.now())



class Settings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_of_shop = db.Column(db.String(255), nullable = False, default="POS System")
    address_of_shop = db.Column(db.Text, nullable=False, default = "Carmona Cavite")
    contact_information = db.Column(db.String(30), nullable = False, default = "09123456789")
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __init__(self, name_of_shop, address_of_shop, contact_information):
        self.name_of_shop = name_of_shop
        self.address_of_shop = address_of_shop
        self.contact_information = contact_information

    
# class Purchase(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     timestamp = db.Column(db.DateTime, default= datetime.now())


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), default = 'closed')
    timestamp = db.Column(db.DateTime, default= datetime.now())

    def __repr__(self):
        return f'{self.amount}'

    def __init__(self, amount):
        self.amount = amount


########################## database END ################################
########################################################################


########################## ADMIN SECTION ###############################

class InventoryView(AdminIndexView):
    def is_visible(self):
        if 'admin' or 'staff' in session:
            return False
    
    @expose('/')
    def index(self):
        user = session.get('admin', None)
        daily_sales = db.session.query(func.sum(Invoice.amount)).all()
        new_result = str(daily_sales).strip('[](),')

        daily_average_sales = db.session.query(func.avg(Invoice.amount)).all()
        new_average_daily = str(daily_average_sales).strip('[](),')

        critical_stocks = Stock.query.all()

        count_invoices = db.session.query(func.count(Invoice.amount)).all()
        new_count_invoices = str(count_invoices).strip('[](),')

        return self.render('admin/reports.html', new_count_invoices = new_count_invoices,new_result = new_result, new_average_daily = new_average_daily, critical_stocks = critical_stocks)



# class ProductView(ModelView):
#     page_size=25
#     column_searchable_list = ['name',]
#     create_modal = True
#     edit_modal = True
#     column_display_pk = True
#     column_hide_backrefs = False
#     can_export = True
#     can_edit = True
#     form_excluded_columns = ['timestamp', 'stock',]
#     column_list = ['category_id','brand','name', 'comment', 'unit_price',]

#     def is_accessible(self):
#         if 'admin' or 'staff' in session:
#             return True
#         return False

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('index'))

class BrandView(ModelView):
    page_size = 25
    column_searchable_list = ['name',]
    form_excluded_columns = ['timestamp']
    column_display_pk = True
    column_hide_backrefs = False


class CategoryView(BaseView):
    @expose('/', methods = ['POST', 'GET'])
    def index(self):
        types = []
        brand = []
        with open('lookups/category.csv') as lookup:
            reader = csv.reader(lookup)
            data = [i.strip() for i in lookup] 
        brands = BrandName.query.all()
        for i in brands:
            brand.append(i)
        if request.method =='POST':
            category = request.form['category']
            if category and request.method =='POST':
               res = Type.query.filter_by(category=category.strip()).all()
               for i in res:
                    types.append(i)
                    print('TYPES=',i)
        
        all_categories = Category.query.all()

        return self.render('admin/category.html', data = data, types = types, brand = brand, all_categories = all_categories)

    def is_accessible(self):
        if 'admin' or 'staff' in session:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))    


class InvoiceView(ModelView):
    page_size = 25
    column_searchable_list = ['timestamp']
    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))    


class SettingsView(ModelView):
    form_excluded_columns = ['timestamp']

    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

    def inaccesible_callback(self, name, **kwargs):
        return redirect(url_for('index'))    

class StocksView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ['id','category', 'received_quantity' , 'quantity', 'timestamp',]
    column_searchable_list = ['id', 'quantity',]
    column_display_pk = True
    column_hide_backrefs = True


    def is_accessible(self):
        if 'admin' or 'staff' in session:
            return True
        return False
   

#WIP 


class ReportsView(AdminIndexView):
    @expose('/')
    def reports_view(self):

        daily_sales = db.session.query(func.sum(Invoice.amount)).all()
        new_result = str(daily_sales).strip('[](),')

        daily_average_sales = db.session.query(func.avg(Invoice.amount)).all()
        new_average_daily = str(daily_average_sales).strip('[](),')

        critical_stocks = db.session.query(Category).all()
        new_critical_stocks = str(critical_stocks).strip('[](),')

        count_invoices = db.session.query(func.count(Invoice.amount)).all()
        new_count_invoices = str(count_invoices).strip('[](),')
        
        return self.render('admin/reports.html',new_count_invoices = new_count_invoices,new_result = new_result, new_average_daily = new_average_daily, critical_stocks = new_critical_stocks)

    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

# class LogoutView(BaseView):
#     @expose('/')
#     def logout(self):
#         return self.redirect(url_for('logout'))

#     def is_accessible(self):
#         if 'admin' in session:
#             return True
#         return False

# # merged view of POS september 24, 2023
class POSView(BaseView):
    @expose('/', methods = ['POST', 'GET'])
    def pos_view(self):
        global arr
        global qty
        global subtotal
        total = session['total']
        if request.method == 'POST':
            barcode = request.form['barcode']
            quantity = request.form['qty']
            if barcode and quantity and request.method == 'POST':
                item = Product.query.filter_by(product_code=barcode).first()
                if item:
                    
                    data = [item.product_code, item.name,int(quantity), item.unit_price]
                    arr.append(data)
                    qty = quantity
                    sum_of_qty = int(qty) * item.unit_price
                    subtotal.append(sum_of_qty)
                    total = sum(subtotal)
                    return render_template('pos.html', arr = arr, qty = qty, total = total)
                flash('not found')
                return redirect(url_for('admin.static', arr = arr, qty = qty, total = total))
        return self.render('pos.html')


class SalesView(BaseView):
    @expose('/')
    def sales_view(self):
        daily_sales = db.session.query(func.avg(Invoice.amount)).all()
        print('daily_sales=',str(daily_sales).strip('[](),'))
        daily_invoices = db.session.query(Invoice).count()
        print('sales=',daily_sales)
        print('invoices=',daily_invoices)
        return self.render('admin/home.html',daily_invoices=daily_invoices, daily_sales=str(daily_sales).strip('[] () ,'))


    def is_accessible(self):
        if 'admin' in session:
            return True
        return False

class StaffView(ModelView):
    form_excluded_columns = ['timestamp',]
    column_list = ['username', 'last_name', 'first_name','email']

    def is_accessible(self):
        if 'admin' in session:
            return True
        return False


admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view = InventoryView())
admin.add_view(CategoryView(name='Category', endpoint='category'))
admin.add_view(StocksView(Stock,db.session))
admin.add_view(InvoiceView(Invoice, db.session))
admin.add_view(StaffView(Staff, db.session))
admin.add_view(SettingsView(Settings, db.session))





##########################   END ADMIN     ###################################
##############################################################################
@app.route('/', methods =['GET', 'POST'])
def index():
    print('index is called!!')
    settings = Settings.query.limit(1).all()
    user = session.get('cashier', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password and request.method =='POST':
            
            staff = Staff.query.filter_by(username=username).first() #unable to login
            print(staff, ' is called!!')
            if staff:
                if staff.password == password:

                    session['cashier'] = username
                    print('cashier is=',user)
                    return redirect(url_for('pos', user = user))
                    flash('User ID or password is incorrect!')
                flash('Incorrect username or password!')
                return redirect(url_for('index'))
            print('unablr to find account')

    return render_template('staff_index.html', settings = settings, user = user)


##################  cashier forgot password ####################################
@app.route('/forgot-password', methods = ['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        if email and request.method == 'POST':
            verify_staff = Staff.query.filter_by(email = email).first()
            if verify_staff:
                session['email'] = email
                return redirect(url_for('reset_password'))
            flash('Incorrect email')
            return redirect(url_for('forgot_password'))

    return render_template('forgot-password.html')




@app.route('/reset-password', methods = ['POST', 'GET'])
def reset_password():
    if 'email' in session:
        email = session.get('email', None)
        if request.method == 'POST':
            pssword = request.form['password']
            confirm = request.form['confirm']
            if pssword and confirm and request.method == 'POST':
                if pssword == confirm:
                    staff = Staff.query.filter_by(email = email).first()
                    if staff:
                        staff.password = pssword
                        db.session.commit()
                        flash('Password update successful!')
                        return redirect(url_for('index'))
                    flash('Problem occured!')
                    return redirect(request.url)
        return render_template('reset-password.html')
    return redirect(url_for('index'))

################# WIP ##########################################################


@app.route('/admin/login', methods = ['GET', 'POST'])
def admin_index():
    staff_username = 'staff'
    staff_password = 'staff@123'
    if 'admin' in session:
        return redirect(url_for('pos'))
    global attempts
    flag = False
    user = session.get('admin', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password and request.method =='POST':
            attempts = attempts + 1
            if username == 'admin' and password == '%12345@':
                session['admin'] = username
                print('admin is=',user)
                return redirect(url_for('pos', user=user))
            elif username == staff_username and password == staff_password:
                session['staff'] = username
                return redirect(url_for('admin.index'))
            
            # if attempts == 3:
            #     flag = True
            #     flash('Temporarilyy disabled login!')
            # while flag:
            #     mins, secs = divmod(1, 20)
            #     timer = '{:02d}:{:02d}'.format(mins, secs)
            #     time.sleep(1)
            #     secs -=1
                # if secs == 0:
                #     flag = False
                #     attempts = 0


            flash('incorrect username or password!')
            return redirect(url_for('admin_index'))
    settings = Settings.query.limit(1).all()
    print('user is=', user)
    return render_template('index.html', settings = settings, user = user)



#add new category
@app.route('/add-category', methods = ['POST'])
def add_category():
    if request.method == 'POST':
        category = request.form['category1']
        types = request.form['type']
        brand = request.form['brand']
        quantity = request.form['quantity']
        comment = request.form['comment']

        if category and types and brand and quantity and comment and request.method =='POST':
            data = Category(category,types,brand,quantity,comment)
            db.session.add(data)
            db.session.commit()
            # print('picked up data=', category, types, brand, quantity, comment)
            return redirect('http://localhost:5000/admin/category')
        return redirect('http://localhost:5000/admin/category')


@app.route('/sales')
@login_required
def sales():
    user = session.get('admin', None)
    daily_sales = db.session.query(func.avg(Invoice.amount)).all()

    print('daily_sales=',str(daily_sales).strip('[](),'))

    daily_invoices = db.session.query(Invoice).count()
    return render_template('sales.html', user = user,daily_invoices=daily_invoices, daily_sales=str(daily_sales).strip('[] () ,'))

#inventory routes here ############################################
@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')


#POST REQUEST ARE REQUIRED FOR THESE ENDPOINTS
#endpoint where the out of stocks quantity would be replenished
@app.route('/replenish', methods = ['POST', 'GET'])
@login_required
def replenish():
    if request.method =='POST':
        pass
    product_to_replenish = Product.query.all()
    return redirect(url_for('inventory'), product_to_replenish = product_to_replenish)
#endpoiunt where a new product would be enlisted into the database
@app.route('/new', methods = ['POST'])
@login_required
def new():
    if request.method == 'POST':
        pass
        
#endpoint where an existing product details would be modified
@app.route('/edit', methods = ['POST'])
@login_required
def edit():
    if request.method == 'POST':
        pass
#endpoint where an existing product would be permanently deleted from database
@app.route('/delete', methods = ['POST'])
@login_required
def delete():
    if request.method =='POST':
        pass

######################## END INVENTORY ROUTES #####################

@app.route('/reports')
@login_required
def reports():
    user = session.get('admin', None)

    chart_data = Invoice.query.all()

    print("output data= ",chart_data)
    return render_template('reports.html', user = user)

@app.route('/settings', methods = ['POST', 'GET'])
@login_required
def settings():
    user = session.get('admin', None)
    if request.method == 'POST':
        business_name = request.form['business-name']
        address = request.form['address']
        contact = request.form['contact']

        if business_name and address and contact and request.method =='POST':
            setting = Settings.query.all()
            print(setting)
            # setting.name_of_shop = business_name
            # setting.address_of_shop = address
            # setting.contact_information = contact

            db.session.commit()

            flash('Business Information Changed')
    return render_template('settings.html', user = user)


#endpoint for the point of sales methodology
# please refer to the algorithm provided in the documentation.
#the pos only accepts cash payments

# would develop functions for gcash/ maya or bank transfers.

@app.route('/pos', methods = ['GET', 'POST'])
@login_required
def pos():
    admin = session.get('admin', None)
    user = session.get('cashier', None)
    
    all_items = Category.query.all()
    global arr
    global qty
    global subtotal
    global total
    
    if request.method  == 'POST':
        barcode = request.form['barcode']
        quantity = request.form['qty']
        if barcode and quantity and request.method == 'POST':
            cat_id = barcode.split(' ')[0]
            brand_name = barcode.split(' ')[1]
            bcode = barcode.split(' ')[4]
            types = barcode.split(' ')[7]
            data = db.get_or_404(Category, cat_id)
            if data:
                stock = db.get_or_404(Stock,data.id)
                print('in stocks',stock.quantity)
                update_stock = int(stock.quantity) - int(quantity)
                stock.quantity = update_stock
                db.session.commit() 
                #always commit the changes to preserve one way process
                #integrity of stocks
                
                #SUM OF quantities multiplied by unit price

                sum_of_qty = float(quantity) * stock.unit_price
                #logic for displaying the category into the POS gui
                item = [data.name, int(quantity), stock.unit_price, stock.quantity,data.brand, data.types]
                if stock.quantity > 0:
                    #updates the global subtotal value based on the calculation on the POS
                    subtotal += sum_of_qty
                    arr.append(item)


                    return render_template('pos.html', total=subtotal,arr= arr,all_items = all_items, user=user,admin = admin)        
            return render_template('pos.html', total=subtotal, arr= arr,all_items = all_items, user=user)
    return render_template('pos.html',total = subtotal, arr=arr,all_items = all_items, admin = admin, user = user)
    # total = session['total']
    # if request.method == 'POST':
    #     #only replaced BARCODE WITH NAME OF ITEM
    #     barcode = request.form['barcode']
    #     quantity = request.form['qty']
    #     if barcode and quantity and request.method == 'POST':
    #         #WIP
    #         item = Product.query.filter_by(name=barcode).first()
    #         if item:
    #             #stock query ===========================================
    #             stock = Stock.query.filter_by(id=item.id).first()
    #             if stock: #if stock exists
    #                 updated_stock = int(stock.quantity) - int(quantity)
    #                 stock.quantity = updated_stock
    #                 db.session.commit()
    #                 #WIP
    #             #=======================================================
    #             data = [item.name,int(quantity), item.unit_price, stock.quantity, item.category_id, item.brand]
    #             print("output data=")
    #             print(data)
    #             if stock.quantity > 0:
    #                 arr.append(data)
    #                 qty = quantity
    #                 sum_of_qty = int(qty) * item.unit_price
    #                 #WIP 
    #                 try:
    #                     subtotal.append(sum_of_qty)
    #                     total += sum_of_qty
    #                     total = sum(subtotal)
    #                 except Exception as e:
    #                     # total += sum_of_qty
    #                     # total = sum(subtotal)
    #                     print('error here')
    #                 # print('items to be sent to the front END=', arr)
    #             elif int(stock.quantity) < int(quantity):
    #                 no_stock_data = [item.name, int(quantity) * 0, item.unit_price, stock.quantity]
    #                 stock.quantity = 0
    #                 db.session.commit()
    #                 flash(f'{item.name} out of stock')
    #                 arr.append(no_stock_data)
    #                 return render_template('pos.html',all_items = all_items ,arr = arr, qty = qty, total = total, user = user, admin = admin)
    #             # print(arr)
    #             return render_template('pos.html', all_items = all_items,arr = arr, qty = qty, total = total, user = user, admin = admin)
    #         flash('not found')
    #         return redirect(url_for('pos', all_items = all_items, arr = arr, qty = qty, total = total, user = user, admin = admin))
    
    # return render_template('pos.html',arr =arr, all_items = all_items, total = total,user = user, admin = admin)

# @app.route('/test', methods = ['POST'])
# def test():
#     if request.method == 'POST':
#         data = request.get_json()

#         if data and request.method == 'POST':
#             return "DATA SUCCEEDED!!"

#     return "INVALID"


@app.route('/void', methods = ['POST'])
def void():
    global arr
    global qty
    global subtotal
    global total

    if request.method =='POST':
        dt = request.get_json()

        if dt and request.method =='POST':
            data = int(dt['data'])

            unit_p = (arr[data][2])
            unit_quantity = (arr[data][1])

            adjusted_subtotal = float(unit_p) * float(unit_quantity)
            print('adjusted=',adjusted_subtotal)
            arr.pop(data)

            subtotal -= adjusted_subtotal
        return redirect(url_for('pos'))
    return redirect(url_for('pos'))


    # total = 0
    # new_subtotal = [float(j) for j in subtotal]
    # total = sum(new_subtotal) 

    # print('the old total is=',total)
    
    # if request.method == 'POST':
    #     dt = request.get_json()

    #     if dt and request.method =='POST':
    #         print("data have passed to the post api!!!")
    #         new_data = int(dt['data'])

    #         try:
    #             sub = (arr[new_data][3])
    #             total = total - float(sub)
    #             print(total)
    #             subtotal = total
    #             print("the updated total=",subtotal)
    #         except Exception as e:
    #             print(e)
    #         arr.pop(new_data)
    #         print("the total is=", total)
    #         return redirect(url_for('pos', arr = arr, total = total, subtotal = subtotal, qty = qty, admin = admin))
    #     return redirect(url_for('pos', arr = arr,subtotal = subtotal, total = total, qty = qty, admin = admin))
    # return redirect(url_for('pos', arr = arr,subtotal = subtotal, total = total, qty = qty, admin = admin))


# @app.route('/voiditem', methods = ['POST'])
# def voiditem():
#     global arr
#     global qty
#     global subtotal
    
#     if request.method == 'POST'
#     # dt = request.json['data']
    # if dt and request.method =='POST':
    #     print("DATA INSIDE THE POST API")
    #     return redirect(url_for('pos', arr = arr, subtotal = subtotal, qty = qty, admin = admin))
    # # return redirect(url_for('pos', arr = arr, subtotal = subtotal, qty = qty, admin = admin))
    # return redirect(url_for('pos', arr = arr, subtotal = subtotal, qty = qty, admin = admin))

@app.route('/variance', methods =['POST', 'GET'])
def variance():
    admin = session.get('admin', None)
    user = session.get('staff', None)
    if 'admin' in session:
        with open('lookups/category.csv') as lookup:
            reader = csv.reader(lookup)
            data = [i.strip() for i in lookup]

        if request.method == 'POST':
            category = request.form['category']
            types = request.form['type']

            if category and types and request.method =='POST':
                if category and types != '':
                    new_type = Type(types.strip(),category.strip())
                    db.session.add(new_type)
                    db.session.commit()

                    flash(f'new type added for {category}')
                    return render_template('variance.html', data = data, admin = admin, user = user)
                flash('fields cannot be empty!')
                return render_template('variance.html', data = data, admin = admin, user = user)
        return render_template('variance.html', data = data, admin = admin, user = user)
    return redirect(url_for('index'))



@app.route('/brand', methods = ['POST'])
def brand():
    if 'admin' in session:
        if request.method == 'POST':
            brand = request.form['brand']

            if brand and request.method =='POST':
                if brand != '':
                    new_brand = BrandName(brand.strip())
                    db.session.add(new_brand)
                    db.session.commit()
                    flash('new brand name added')
                    return redirect(url_for('variance'))
                flash('field cannot be empty!')
                return redirect(url_for('variance'))
            return redirect(url_for('variance'))
    return redirect(url_for('index'))






@app.route('/cancel', methods = ['POST'])
def cancel():
    global arr
    global qty
    global subtotal
    filename = 'invoice.csv'
    if request.method == 'POST':
        arr = []
        qty = 0
        session['total'] = 0
        subtotal = 0 #changed from list to integer/float

        f = open(filename, 'w+')
        f.close()

        print('array cleared')
        return redirect(url_for('pos'))


@app.route('/checkout', methods = ['POST'])
@login_required
def checkout():
    global arr
    global subtotal
    global total
    subt = 0
    if request.method =='POST':
        subtotal_amount = request.form['subtotal']
        tendered_amount = request.form['amount']
        if subtotal_amount and tendered_amount and request.method == 'POST':

            sub = ''.join(subtotal_amount)
            print('subtotal=', sub)
            print('tendered=', tendered_amount)

            change = float(tendered_amount) - float(sub)

            fl = open('invoice.txt', 'w').close()
            f = open('invoice.txt', 'a')
            f.write('  J AI Office and School Supplies' + '\n')
            f.write('==================================' + '\n')
            # f.write('item'.jlust(0) + 'qty'.center(5) + 'unit p.'.rjust(10))
            for line in arr:
                category = f'{line[4]} {line[0]}{line[5]}'
                f.write("{} {} {} {}".format(category.ljust(0), str(line[2]).center(5), str(line[2]).rjust(10), '\n'))
            f.write('==================================' + '\n')
            f.write('        OFFICIAL RECEIPT          ' + '\n\n')
            f.write('date: ' + str(datetime.now().strftime('%m/%d/%Y- %H:%M')) +'\n')
            f.write('Total Amount:'+ subtotal_amount.rjust(25) + '\n')
            f.write('Amount Tendered: '+ tendered_amount.rjust(20) + '\n')
            f.write('Change: '+ str(change).rjust(27))  
            f.close()
            # clears all the variables
            arr = []
            subtotal = 0
            session['total'] = 0
            total = 0

            webbrowser.open('invoice.txt')

            #saves into database
            new_invoice = Invoice(subtotal_amount)
            db.session.add(new_invoice)
            db.session.commit()

            #prints the txt file to ptinter
            try:
                os.startfile('invoice.txt','print')
            except e as Exception:
                print('error occured!')

        return redirect(url_for('pos'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.before_request
def init_db():
    db.create_all()

    if Settings.query.all() is None:
        default_setting = Settings('POS System', 'Carmona Cavite', '09123456789')
        db.session.add(default_setting)
        db.session.commit()
        print('database created')


#unused codes

# print("BEFORE DATA PROCESSING===", d)
            # flat_list = []
            # for i in d:
            #     for j in i:
            #         flat_list.append(j)
            # flat_list[1:4] = [' '.join(flat_list[1:4])]
            # deleted_last_index = flat_list[:-1]
            # new_arr_last_index_deleted = [i for i[:-1] in arr]
            # new_list2 = [i for i in d if(list(i) != deleted_last_index)]
            # new_list2 = arr.remove(deleted_last_index)
            # filtered_list = [ not i for i in new_arr_last_index_deleted if(list(i) == deleted_last_index)]
            # print("flat list=",deleted_last_index)
            # arr = [i for i in d if (list(i) == deleted_last_index)]
            # print("INPUT DATA AFTER DATA PROCESSING=",d)
            # print("filtered array=", filtered_list)







if __name__ == '__main__':
    app.run(debug=True)