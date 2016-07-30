from flask import render_template, redirect, url_for, request, Response
import json
import datetime
from datetime import datetime as d
from datetime import date
from ceperth import app
from .database import session
from .models import Post, Comment, User, Programs, Task, CellMeeting
from .models import Registrants, Minutes, Member, Cell, Plans, Activities
import mistune
import datetime
from flask import flash
from flask.ext.login import login_user, login_required,current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.mail import Mail, Message
from dates import last_monthstart, last_twomonthstart,\
this_monthstart, thismonth, lastmonth, lasttwomonth


req = lambda y : request.form[y]

@app.route("/cells/<int:id>/achievements", methods = ['GET','POST'])
@login_required
def achievements(id):
    return render_template("achievements.html")

@app.route("/cells/<int:id>/achievements/<slug>", methods = ['GET','POST'])
def cellachievement(id, slug):
    return render_template('singleachievement.html', slug=slug)

@app.route("/delactivity", methods = ['GET', 'POST'])
@login_required
def delactivity():
    reqst = request.form
    if request.method == "POST":
        act_id = reqst['act_id']
        tab = reqst['menu']
        cellid = int(reqst['cellid'])
        actdelete = session.query(Activities).filter_by(id=act_id).one()
        session.delete(actdelete)
        session.commit()
        return redirect(url_for('cellreport', id= cellid, tab=tab))
    else:
        return "Error"

@app.route("/addactivity", methods = ['GET' ,'POST'])
@login_required
def addactivity():
    reqst = request.form
    gx = lambda x: reqst.get(x, '')
    if request.method == 'POST':
        tab = gx('menu')
        cellid = int(gx('cellid'))
        act_date = gx('date')
        act_content = gx('activity')
        act_date = d.strptime(act_date, '%d-%m-%Y').date()
        activity = ""
        if reqst.has_key('add'):
            activity = Activities(
                act_activ = act_content,
                act_date = act_date,
                cell_id = cellid
            )
        elif reqst.has_key('edit'):
            act_id = gx('act_id')
            activity = session.query(Activities).filter_by(id=act_id).first()
            activity.act_date = act_date
            activity.act_activ = act_content 
        session.add(activity)
        session.commit()
        return redirect(url_for('cellreport', id= cellid, tab=tab))
    else:
        return "Error"


@app.route("/addplans", methods = ['GET', 'POST'])
@login_required
def addplans():
    reqst = request.form
    gx = lambda x: reqst.get(x, '')
    if request.method == 'POST':
        tab = gx('menu')
        cellid = int(gx('cellid'))
        rt = reqst.has_key('materials')
        editp = session.query(Plans).filter_by(cell_id= cellid).first()
        editp.prayer = reqst.has_key('prayer') and  gx('prayer') or editp.prayer
        editp.outreach = reqst.has_key('outreach') and  gx('outreach') or editp.outreach
        editp.visitation  = reqst.has_key('visitation') and gx('visitation') or editp.visitation
        editp.fellowship = reqst.has_key('fellowship') and gx('fellowship') or editp.fellowship
        editp.materials = reqst.has_key('materials') and gx('materials') or editp.materials
        editp.others = reqst.has_key('others') and gx('others') or editp.others
        
        session.add(editp)
        session.commit()
        return redirect(url_for('cellreport', id= cellid, tab=tab))
    else:
        return "Error"
    

@app.route("/cells/<int:id>/cellhome", methods = ['GET','POST'])
def cellhome(id):
    plans = session.query(Plans).filter_by(cell_id=id).first()
    return render_template("cellhome.html", plans=plans)

@app.route("/cells/<int:id>/addweekreport", methods = ['GET','POST'])
@login_required
def weekreport(id):
    if request.method == 'POST':
        tab = req('menu')
        cmetdates = request.form['cmetdates']
        cmetdates = d.strptime(cmetdates, '%d-%m-%Y').date()
        cellmeeting = CellMeeting(cmbsgrp = req('cmbsgrp'),
        cmmet = req('cmmet'),
        cmetdates = cmetdates,
        cmoff = req('cmoff'),
        cmft = req('cmft'),
        cmseed = req('cmseed'),
        cmtotalatt = req('cmtotalatt'),
        cmholysprit = req('cmholysprit'),
        cmnewcon = req('cmnewcon'),
        cmnewcells = req('cmnewcells'),
        cmnewbsgrp = req('cmnewcells'),
        cell_id = id)
        session.add(cellmeeting)
        session.commit()
        return redirect(url_for('cellreport', id=id, tab=tab))
    else:
        cell = session.query(Cell).filter_by(id = id).one()
        return render_template('weekreport.html', cell=cell)

@app.route("/cells", methods = ['GET','POST'])
@login_required
def cells():
    cells = session.query(Cell).order_by(Cell.cellname)
    admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
    return render_template('cells.html', cells=cells, admin=admin)

@app.route("/cells/members/<int:id>", methods = ['GET','POST'])
@login_required
def singlemembreport(id):
    cellmember = session.query(Member).filter_by(id = id).first()
    if request.method == 'POST':
        tab = req('menu')
        cellmember.memb_wk1 = req('memb_wk1')
        cellmember.memb_wk2 = req('memb_wk2')
        cellmember.memb_wk3 = req('memb_wk3')
        cellmember.memb_wk4 = req('memb_wk4')
        cellmember.memb_wk5 = req('memb_wk5')
        cellmember.memb_comment = req('memb_comment')
        session.add(cellmember)
        session.commit()
        return redirect(url_for('cellreport', id=cellmember.cell_id, tab=tab))
    else:

        return render_template('singlecellreport.html', mem=cellmember,
                cellid =cellmember.cell_id)

@app.route("/cells/<int:id>/cellreports", methods = ['GET','POST'])
@login_required
def cellreport(id):
    
    if request.method == 'POST':
        cell_id = req('cellid')
        member = Member(memb_name = req('memb_name'),
            memb_address = req('memb_address'),
            memb_email = req('memb_email'),
            memb_contact = req('memb_contact'),
            memb_comment = req('memb_comment'),
            cell_id = cell_id
            )

        session.add(member)
        session.commit()
        return redirect(url_for('cells', id=cell_id))
    
    else:
        tab = request.values.get('tab', '')
        monthact = session.query(Activities).filter_by(cell_id = id)
        monthact = monthact.order_by(Activities.act_date)
        plans = session.query(Plans).filter_by(cell_id=id).first()
        cells = session.query(Cell)
        cell = session.query(Cell).filter_by(id = id).one()
        cellall = session.query(CellMeeting).filter_by(cell_id = id)
       
        dic = {}
        tm_cell = cellall.filter(CellMeeting.cmetdates >= this_monthstart())
        
        lm_cell = cellall.filter(CellMeeting.cmetdates >= last_monthstart())
        lm_cell = lm_cell.filter(CellMeeting.cmetdates < this_monthstart())
       
        ltm_cell = cellall.filter(CellMeeting.cmetdates >= last_twomonthstart())
        ltm_cell = ltm_cell.filter(CellMeeting.cmetdates < last_monthstart())
        
        monthtitle = [thismonth, lastmonth,lasttwomonth]
                          
        monthdic = [{'tm':{}}, {'lm': {}}, {'ltm':{}}]
        monthobj = [tm_cell,  lm_cell, ltm_cell]
        member = session.query(Member).filter_by(cell_id=id).order_by(Member.memb_name)
        
        for monobj, dic, mntitle in zip(monthobj, monthdic, monthtitle):
            contentdict = {}
            dummydict = {}
            try:
                mm_cmet = [inp.cmmet for inp in monobj.all()]
                mm_cmet = 'Y' in mm_cmet and 'Y' or 'N'
                contentdict["cellmet"] = mm_cmet
            
                mm_bs = monobj.order_by(CellMeeting.cmbsgrp.desc()).first()
                contentdict["bsgrp"] = mm_bs.cmbsgrp
           
                mm_ta = monobj.order_by(CellMeeting.cmtotalatt.desc()).first()
                contentdict["highestatt"] = mm_ta.cmtotalatt
            
                mm_ft = [val.cmft for val in monobj.all()]
                mm_ft = sum(mm_ft)
                contentdict["totalft"] = mm_ft
            
                mm_nc = [inp2.cmnewcon for inp2 in monobj.all()]
                mm_nc = sum(mm_nc)
                contentdict["totalnc"] = mm_nc
            
                mm_hs = [inp3.cmholysprit for inp3 in monobj.all()]
                mm_hs = sum(mm_hs)
                contentdict["totalhs"] = mm_hs
            
                mm_off = [inp4.cmoff for inp4 in monobj.all()]
                mm_off = sum(mm_off)
                contentdict["totaloff"] = mm_off
            
                mm_seed = [inp5.cmseed for inp5 in monobj.all()]
                mm_off = sum(mm_seed)
                contentdict["totalseed"] = mm_off
            
                mm_ncells = [inp6.cmnewcells for inp6 in monobj.all()]
                mm_ncells = sum(mm_ncells)
                contentdict["totalncells"] = mm_ncells
            
                mm_newbs = [inp6.cmnewbsgrp for inp6 in monobj.all()]
                mm_newbs = sum(mm_newbs)
                contentdict["totalnewbs"] = mm_newbs
            
                cell_ms = len(member.all())
                contentdict["totalms"] = cell_ms
            except:
                pass
            
            finally:
                contentdict["mntitle"] = mntitle
                dummydict.update(contentdict)
            
            for key, val in dic.iteritems():
                dic[key] = dummydict
    
    return render_template('cellreport.html', member = member, cell = cell,
                           thm = thismonth, cells = cells, cellall = cellall,
                           monthdic = monthdic, plans=plans, tab=tab,
                           monthact = monthact)


@app.route("/delnotes", methods = ['GET','POST'])
@login_required
def deleteminutes():
    if request.method =='POST':
        noteid = request.form['deleteitem'] 
        notedeleting = session.query(Minutes).filter_by(id = int(noteid)).one()
        session.delete(notedeleting)
        session.commit()
        return redirect(url_for('leadersnotes'))
    else:
        return "Error"

@app.route("/leaders/notes/", methods= ['GET', 'POST'])
@login_required
def leadersnotes():
    minutes = session.query(Minutes).order_by(Minutes.meetingdate.desc())
    if request.method == 'POST':
        minute = Minutes(
        content = req('content')
        )
        session.add(minute)
        session.commit()

        details = "The action notes from the leaders meeting has been Posted. Please do review and act accordignly. Thanks. ...View full message on CEPerthForum!"
        members = session.query(User).all()
        all_members = [str(member.email) for member in members]
        mail=Mail(app)
        with mail.connect() as conn:
            for email in all_members:
                message = Message(subject="Leaders Action Note has been posted by "+ current_user.name,
                    body= details,
                    sender=("CEPerthForum", "kesfrance@gmail.com"),
                    recipients=[email]
                    )

                conn.send(message)

        return redirect(url_for('leadersnotes'))
    else:
        return render_template('leadersnote.html', minutes = minutes)


@app.route("/registration/<int:id>", methods= ['GET', 'POST'])
@login_required
def registrations(id):
    if request.method == 'POST':
        register = Registrants(
        regisdate = date.today(),
        regisname = request.form['name'],
        regisnum = request.form['number'],
        regisfollow = request.form['status'],
        followcomment =request.form['comment'],
        regisemail = request.form['email'],
        regismode = request.form['mode'],
        regisadress =request.form['address'],
        regisdoer_id = int(request.form['doer']),
        program_id = id)
        session.add(register)
        session.commit()
        return redirect(url_for('registrations', id=id))
    else:
        siprog = session.query(Programs).filter_by(id=id).one()
        #task = session.query(Task).filter_by(program_id=siprog.id).order_by(Task.taskdate.desc())
        users = session.query(User).order_by(User.id)
        registered = session.query(Registrants).filter_by(program_id=siprog.id) #order_by(regisdate=Registrants.regisdate.desc)
        num =[]
        for val in registered:
            num.append(val.regisname)
        num = len(num)
        return render_template('registrations.html',
                           id=id, sprog=siprog,
                           num=num, users=users, registered=registered)


@app.route("/programs/add", methods =['GET', 'POST'])
@login_required
def addprogram():
    if request.method == "POST":
        if request.form['progname']:
            program = Programs(
            progname = request.form['progname'],
            progdesc = request.form['progdesc'],
            progaim = request.form['progaim']
            )
            session.add(program)
            session.commit()
        flash("You have created a new program", "info")
        return redirect(url_for('programs'))
    else:
        return render_template("addprograms.html")

@app.route("/programs", methods =['GET', 'POST'])
@login_required
def programs():
    if request.method == "POST":
        if  request.form['progname']:
            program = Programs(
            progname = request.form['progname'],
            progdesc = request.form['progdesc'],
            progaim = request.form['progaim']
            )

            session.add(program)
            session.commit()
        return redirect(url_for('programs'))
    else:
        prog = session.query(Programs).order_by(Programs.id)
        admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
        return render_template("programs.html", prog=prog, admin=admin)

@app.route("/delprograms", methods = ['GET','POST'])
@login_required
def delprogramPost():
    if request.method =='POST':
        progid = request.form['deleteitem'] #request.form['program_id'])
        progdel = session.query(Programs).filter_by(id = int(progid)).one()
        session.delete(progdel)
        session.commit()
        return redirect(url_for('programs'))
    else:
        return "Error"


@app.route("/program/<int:id>", methods=['GET', 'POST'])
@login_required
def single_program(id):
    if request.method == "POST":
        if request.form['taskname']:
            ddate = request.form['duedate']
            ddate = d.strptime(ddate, '%d-%m-%Y').date()
            task = Task(
            taskdate = date.today(),
            taskname = request.form['taskname'],
            taskcomment = request.form['taskcomment'],
            taskstatus = request.form['taskstatus'],
            duedate = ddate,
            taskdoer_id = int(request.form['taskdoer']),
            program_id = id )
            session.add(task)
            session.commit()

        return redirect(url_for('single_program', id=id))
    else:
        siprog = session.query(Programs).filter_by(id=id).one()
        task = session.query(Task).filter_by(program_id=siprog.id).order_by(Task.taskdate.desc())
        users = session.query(User).order_by(User.id)
    return render_template('singleprogram.html',
                           id=id, sprog=siprog,
                           task=task, users=users)

@app.route("/post")
@app.route("/page/<int:page>")
@login_required
def posts(page=1, paginate_by=7):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]
    admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        admin = admin
    )
@app.route("/")
def main():
    return redirect(url_for("login_get"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    flash("You have logged in", "info")
    return redirect(request.args.get('next') or url_for("posts"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login_get'))



@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    members = session.query(User).all()
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        description = request.form["description"],
        author=current_user
    )
    session.add(post)
    session.commit()
    all_members = []
    for member in members:
        all_members.append(member.email)
    all_members = [str(i) for i in all_members]
    describe = request.form["description"] +".... View full message on TeamForum!"
    mail=Mail(app)
    with mail.connect() as conn:
      for email in all_members:
        message = Message(subject="A new forum has been created by "+ current_user.name,
                  body= describe,
                  sender=("TeamForum", "kesfrance@gmail.com"),
                  recipients=[email]
                 )

        conn.send(message)

    flash("You have created a new forum. Team members have been notified.", "info")
    return redirect(url_for("posts"))

#view for single post
@app.route("/post/<int:id>", methods=['GET'])
def singlepost_get(id):
    try:
        post = session.query(Post).filter_by(id=id).one()
        comments = session.query(Comment).filter_by(post_id=post.id)
        comments = comments.order_by(Comment.datetime.desc()).all()
        admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()

        return render_template("singlepost.html",
                           post=post,
                           id=id,
                           comments=comments,
                           admin = admin
                          )
    except:
          error_msg = "Sorry, the page you are trying to view doesn't exist."
          return render_template("error.html",error_msg=error_msg)

@app.route("/post/<int:id>", methods= ['POST'])
@login_required
def singlepost_comment(id):
    post = session.query(Post).filter_by(id=id).one()
    comments = session.query(Comment).filter_by(post_id=post.id).all()

    #mail list of people who commented on a forum, dont include comment author
    participants = list(set([str(i.author.email) for i in comments
                            if i.author.email != current_user.email]))

    #if the current user is not the creator of forum, add forum creator to list
    if post.author.email != current_user.email:
        participants.append(str(post.author.email))

    content = request.form["content"][:30] + "....View full message on TeamForum."

    comment = Comment(
        post=session.query(Post).get(id),
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(comment)
    session.commit()

    if len(participants) != 0:
      mail=Mail(app)
      with mail.connect() as conn:
          for email in list(set(participants)):
            message = Message(subject= current_user.name + " made a comment on "
                  + post.title, body= content,
                  sender=("TeamForum", "kesfrance@gmail.com"),
                  recipients=[email]
                 )

            conn.send(message)

    flash("You've posted a comment. Paricipants will be notified", "info")

    return redirect(url_for("singlepost_get", id=id))

@app.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])
def editComment(comment_id):
    commentToEdit= session.query(Comment).filter_by(id=comment_id).one()
    if request.method == 'POST':
        if request.form['content']:
            commentToEdit.content = request.form['content']
            commentToEdit.datetime = datetime.datetime.now()
            session.add(commentToEdit)
            session.commit()
        flash("You have editted your comment", "info")
        return redirect(url_for('posts'))
    else:
        return render_template('editcomment .html', p=commentToEdit)

@app.route("/comment/<int:comment_id>/delete", methods=['GET', 'POST'])
def deleteComment(comment_id):
    commentToDelete = session.query(Comment).filter_by(id=comment_id).one()
    if request.method == 'POST':
        session.delete(commentToDelete)
        session.commit()
        flash("You have deleted your comment", "info")
        return redirect(url_for('posts'))
    else:
        return render_template('deletecomment.html', i=commentToDelete)


@app.route("/post/<int:id>/edit", methods=['GET', 'POST'])
def editpost(id):
    postToEdit= session.query(Post).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['title']:
            postToEdit.title = request.form['title']
            postToEdit.content = request.form['content']
            postToEdit.datetime = datetime.datetime.now()
            session.add(postToEdit)
            session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template('editpost.html', p=postToEdit)

@app.route("/post/<int:id>/delete", methods = ["GET", "POST"])
def deletepost(id):
    postToDelete = session.query(Post).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(postToDelete)
        session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template('deletepost.html', i=postToDelete)


@app.route("/dosignup", methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route("/dosignup", methods=["POST"])
def signup_post():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    password_2=request.form["re-password"]

    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("signup_get"))

    if not (password and password_2) or password != password_2:
        flash("Passwords did not match", "danger")
        return redirect(url_for("signup_get"))

    user = User(name=name, email=email, password=generate_password_hash(password))

    session.add(user)
    session.commit()

    flash("Success! You may now login with your credentials", "info")
    return redirect(url_for("login_get"))


@app.route("/post/JSON", methods=["GET"])
@login_required
def posts_get():
    """ Get a list of posts """
    posts = session.query(Post).order_by(Post.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/post/<int:id>/JSON", methods=["GET"])
@login_required
def post_get(id):
    """ Single post endpoint """
    post = session.query(Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")

@app.route("/post/names/all/all")
def query():
   users = session.query(User).order_by(User.id)
   return render_template("users.html", users=users)

@app.route("/registered/all/all")
def getMails():
    registered = session.query(Registrants)
    return render_template("registerdetails.html", registered=registered)



