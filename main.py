from flask import Flask,render_template,request
import json
import re
pattern = '<[^<]+?>'
import hashlib
import os
app=Flask('app')
@app.route("/")
def index():
  return render_template("index.html")
@app.route("/admin")
def admin():
  return render_template("admin.html")
@app.route("/features/navbar")
def navbar():
  print("Returning navbar")
  with open("navbar.txt") as f:
    navbar=f.read()
  return navbar
@app.route("/admin/login")
def admin_login():
  username=request.headers.get("username")
  password=request.headers.get("password")
  file=f"admin_data/{username.lower()}.json"
  if os.path.exists(file):
    with open(file) as f:
      admin_data=json.load(f)
    password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password==admin_data['password']:
      with open("admin_data/adminpage.txt") as f:
        html=f.read()
      with open("admin_data/newscripts.txt") as s:
        js=s.read()
      with open("database/categories.json") as f:
        file=json.load(f)
        categories=file['categories']
      return {"success":True,"data":admin_data,"admin_page":html,"newscripts":js,"categories":categories}
    else:
      return{"success":False,"reason":"Password Incorrect"}
  else: 
    return {"success":False,"reason":"User Does Not Exist"}
@app.route("/admin/categories/new")
def new_categorie():
  username=request.args.get("username")
  password=request.args.get("password")
  category=request.args.get("cat")
  file=f"admin_data/{username.lower()}.json"
  if os.path.exists(file):
    with open(file) as f:
      admin_data=json.load(f)
    password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password==admin_data['password']:
      with open("database/categories.json") as f:
        data=json.load(f)
        print(data)
        for a in data['categories']:
          print(a)
          if a.lower()==category.lower():
            return {"success":False,"result":"That category already exists"}
        data['categories'].append(category.lower())
      with open("database/categories.json","w") as f:
        keepdata=data
        json.dump(data,f)
      return {"success":True,"result":"Added new category","action":"refresh","data":keepdata}
    else:
      return {"success":False,"result":"Incorrect Login"}
  else:
    return {"success":False,"result":"Incorrect Login"}
@app.route("/categories/get")
def get_categories():
  with open("database/categories.json") as f:
    data=json.load(f)
  return data
@app.route('/articles/get-recent')
def get_recent():
  with open("database/recent.json") as f:
    data=json.load(f)
  return data
@app.route("/search")
def search():
  return render_template("search.html")
@app.route("/searchdatabase")
def search_articles():
  query=request.args.get("query")
  results=[]
  querys=query.split()
  with open('database/article_names.json') as f:
    articles=json.load(f)
  for q in querys:
    for a in articles['articles']:
      articlename=a['name'].split()
      aname=[]
      for t in articlename:
        name=t.lower()
        aname.append(name)
      if q.lower() in aname:
        if not a in results:
          results.append(a)
  return {"results":results}
@app.route("/articles/read")
def read_article():
  return render_template("read.html")
@app.route("/articles/read/get-article")
def get_article():
  category=request.args.get("category")
  name=request.args.get("name")
  file=f"database/{category}/{name}.json"
  if os.path.exists(file):
    with open(file) as f:
      data=json.load(f)
    return {"success":True,"article":data}
  else:
    return {"success":False,"result":"This article does not exist"}
@app.route("/admin/articles/postarticle",methods = ['POST'])
def post_article():
  data=request.data
  my_json = data.decode('utf8')
  data=json.loads(data)
  file=f"database/{data['category'].lower()}"
  if not os.path.isdir(file):
    os.mkdir(file)
  article=f"database/{data['category'].lower()}/{data['article_name']}.json"
  if os.path.exists(article):
    return {'success':False,"result":"Article with that name exists already"}
  with open(article,"w") as f:
    json.dump(data,f)
  articledata=data
  with open('database/recent.json') as f:
    data=json.load(f)
  if len(data['recent'])>=5:
    data['recent'].pop(0)
  snippet=""
  arraydata=articledata['article'].split()
  for a in range(0,len(arraydata)):
    if not a>45:
      snippet+=f"{arraydata[a]} "
    else:
      snippet+="..."
      break
  outputString = re.sub(pattern, "", snippet)
  data['recent'].append({'name':articledata['article_name'],"date":articledata['date'],"author":articledata['author'],"snippet":outputString,"category":articledata['category']})
  with open('database/recent.json',"w") as f:
    json.dump(data,f)
  with open("database/article_names.json") as t:
    names=json.load(t)
    names['articles'].append({"name":articledata['article_name'],"category":articledata['category']})
  with open("database/article_names.json","w") as f:
    json.dump(names,f)
  return {"success":True,"result":"Article published"}
app.run(host="0.0.0.0",port="6000")