import os
import datetime
from datetime import date
from flask.ext.script import Manager
from ceperth import app
from ceperth.models import Post, Programs, Task, Registrants, Minutes, Member, \
    Cell, CellMeeting, Plans
from ceperth.database import session as DBsession

from getpass import getpass
from werkzeug.security import generate_password_hash
from ceperth.models import User

from flask.ext.migrate import Migrate, MigrateCommand
from ceperth.database import Base


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

#add dummy post to databse
@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    for i in range(1,26):
        post = Post(
            title="Test Post #{}".format(i),
            content=content            
        )
        DBsession.add(post)
    DBsession.commit()

@manager.command
def register():
    register = Registrants(
    regisdate = date.today(),
    regisname = "Andrew Menu",
    regisnum = "o404555",
    regisfollow = 'Undone',
    followcomment ="still working on",
    regisemail = "kesemai@y.com",
    regismode = 'inperson',
    regisadress ='54 Gordona pde',
    regisdoer_id = 1,
    program_id = 1
)
    DBsession.add(register)
    DBsession.commit()
    
@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()   

@manager.command
def program():
    program = Programs(
        progdate = date.today(),
        progname = "Achievers Night",
        progdesc = "A two day information and networking meeting for youths",
        progaim = "This will be a two day information and networking meeting for young adults in the team",
    )
    DBsession.add(program)
    DBsession.commit()

@manager.command
def addtask():
    task = Task(
        taskdate = date.today(),
        taskname = "Print T shirts",
        taskstatus = "Sent to Freo TShirt",
        duedate = date.today() + datetime.timedelta(days=14),
        taskdoer_id = 2,
        program_id = 2
    )
    DBsession.add(task)
    DBsession.commit()

@manager.command
def cellmember():
    member = Member(memb_name = 'Goerge',
            memb_address = "Morley Drive",
            memb_email = "smuzungu@yahoo.com",
            memb_contact = "040474449",
            cell_id = 2
            )

    DBsession.add(member)
    DBsession.commit()

@manager.command
def addminutes():
    minute = Minutes(
        content = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )
    DBsession.add(minute)
    DBsession.commit()
   
@manager.command
def addcell():
    cell = Cell (cellname = "Zoe",
        cellleader = "Sis Nichola & Kasansa",
        cellcode = 106,
    )
    DBsession.add(cell)
    DBsession.commit()

@manager.command
def cell_meeting():
    cellmeeting = CellMeeting(cmbsgrp = 1,
        cmmet = 'Y',
        cmetdates = "2016-05-18",
        cmoff = 10,
        cmft = 0,
        cmseed = 10,
        cmholysprit = 0,
        cmnewcon = 0,
        cmnewcells = 1,
        cmnewbsgrp = 1,
        cell_id = 1
    )
    DBsession.add(cellmeeting)
    DBsession.commit()

@manager.command
def add_plan():
    plan = Plans(prayer = "two days a week",
    outreach = "Wednesday and fridays",
    visitation = "visit leanne",
    fellowship = "at pastors house",
    materials = "Power of your mind",
    others = "none at the moment",
    cell_id = 1
    )
    DBsession.add(plan)
    DBsession.commit()
    
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


    
if __name__ == '__main__':
    manager.run()



#if __name__ == '__main__':
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)
