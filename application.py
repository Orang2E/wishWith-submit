from flask import Flask, render_template , url_for, request, redirect , flash, session
from database import DBhandler
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"]="helloosp"
DB = DBhandler()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/login')
def login():
    return render_template('login.html')





@app.route("/product-add") 
def productAdd():
    return render_template('product_add.html')

@app.route("/header-before")
def headerBefore():
    return render_template('layout/header_before.html')
@app.route("/header-after")
def headerAfter():
    return render_template('layout/header_after.html')

@app.route("/add-product-post", methods=["POST"])
def registerproduct():
    print(request.form)  # 확인용 출력
    print(request.files)  # 확인용 출력
    image_file = request.files["img_path"]
    image_file.save("static/img/{}".format(image_file.filename))
    data = {
        "product_description": request.form.get("product-description"),
        "product_place": request.form.get("product-place"),
        "product_number": request.form.get("product-number"),
        "product_category": request.form.get("product-category"),
        "start_date": request.form.get("start-date"),
        "end_date": request.form.get("end-date"),
        "img_path": "static/img/" + image_file.filename
    }
    DB.insert_item(data['product_category'], data, image_file.filename)
    return render_template("products_list.html", data={ "img_path": "static/img/" + image_file.filename, **data })

@app.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 6  # item count to display per page
    per_row = 3  # item count to display per row   
    start_idx=per_page*page
    end_idx=per_page*(page+1)
   
    data = DB.get_items()  # read the table
    
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    
    row_data = [list(data.items())[i * per_row:(i + 1) * per_row] for i in range(per_page // per_row)]

    return render_template("list.html", row_data=row_data, limit=per_page,page=page, page_count=int((item_counts/per_page)+1),total=item_counts)



@app.route("/view_detail/<name>/")
def view_item_detail(name):
        data = DB.get_item_byname(str(name))
        return render_template("detail.html", name=name, data=data)


@app.route("/product-detail")
def productDetail():
    return render_template('product_detail.html')

@app.route("/products-list")
def productsList():
    return render_template('products_list.html')





@app.route("/review-add") 
def reviewAdd():
    return render_template('review_add.html')

@app.route("/review-detail")
def reviewDetail():
    return render_template('review_detail.html')

@app.route("/reviews-list")
def reviewList():
    return render_template('reviews_list.html')

@app.route("/signup1")
def signup1():
    return render_template('signup1.html')

@app.route("/signup2", methods=["GET", "POST"])
def signup2():
    if request.method == "POST":
        return redirect(url_for('signup1'))
    return render_template('signup2.html')



@app.route("/signup1_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data, pw_hash):
        return render_template('signup3.html')
    else:
        flash("이미 존재하는 아이디입니다!")
        return redirect(url_for('signup1'))
    
@app.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('index'))
    else:
        flash("존재하지 않는 정보입니다! 다시 로그인을 시도해주세요.")
        return redirect(url_for('login'))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)