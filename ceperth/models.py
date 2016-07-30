import datetime
from datetime import date
from sqlalchemy import Column, Integer, String, Text, DateTime,\
ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from .database import Base, engine
from flask.ext.login import UserMixin



class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    #superuser = Column(Boolean, default='False')
    posts = relationship("Post", backref="author")
    comments = relationship("Comment", backref="author")
    tasks = relationship("Task", backref='taskdoer')
    registrants = relationship("Registrants", backref="registrar")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    description = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    #pats = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey('users.id'))
    comments = relationship("Comment", backref="post")

    def as_dictionary(self):
        datetime = self.datetime.strftime("%d/%m/%y")
        post= {
            "title": self.title,
            "id": self.id,
            "datetime": datetime,
            "content": self.content,
            "description" : self.description
          }
        return post

class Comment(Base):
    __tablename__= "comments"
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

class Programs(Base):
    __tablename__= "programs"
    id = Column(Integer, primary_key=True)
    progdate = Column(DateTime, default=date.today())
    progname = Column(String(1024), nullable=False)
    progdesc = Column(Text, nullable=False)
    progaim = Column(Text, nullable=False)
    tasks = relationship("Task", backref="tasks")
    registrants = relationship("Registrants", backref="registrant")

class Task(Base):
    __tablename__="tasks"
    id = Column(Integer, primary_key=True)
    taskdate = Column(DateTime, default=date.today())
    taskname = Column(String(1024), nullable=False)
    taskstatus = Column(String(1024), default='Undone')
    taskcomment =Column(Text, nullable=True)
    duedate = Column(DateTime, nullable=False)
    taskdoer_id = Column(Integer, ForeignKey('users.id'))
    program_id = Column(Integer, ForeignKey('programs.id'))


class Registrants(Base):
    __tablename__="registrant"
    id = Column(Integer, primary_key=True)
    regisdate = Column(DateTime, default=date.today())
    regisname = Column(String(1024), nullable=False)
    regisnum = Column(String(1024), nullable=True)
    regisfollow = Column(String(1024), default='Undone')
    regisadress =Column(Text, nullable=True)
    followcomment =Column(Text, nullable=True)
    regisemail = Column(String(1024), nullable=True)
    regismode = Column(String(1024), default='inperson')
    regisdoer_id = Column(Integer, ForeignKey('users.id'))
    program_id = Column(Integer, ForeignKey('programs.id'))

class Minutes(Base):
    __tablename__="munites"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    meetingdate = Column(DateTime, default=datetime.datetime.now)

class Member(Base):
    __tablename__='cellmember'
    id = Column(Integer, primary_key=True)
    memb_name = Column(String(1024), nullable=False)
    memb_address = Column(String(1024), nullable=True)
    memb_email = Column(String(64), nullable=True)
    memb_contact = Column(String(32), nullable=True)
    memb_foundation = Column(Integer, default=0)
    memb_baptised = Column(Integer, default=0)
    memb_celldate = Column(DateTime, default=date.today())
    memb_wk1 = Column(String(2), default='NM')
    memb_wk2 = Column(String(2), default='NM')
    memb_wk3 = Column(String(2), default='NM')
    memb_wk4 = Column(String(2), default='NM')
    memb_wk5 = Column(String(2), default='NM')
    memb_comment =Column(Text, nullable=True)
    memb_follow = Column(String(1024), default='Undone')
    cell_id = Column(Integer, ForeignKey('cell.id'))

class Cell(Base):
    __tablename__='cell'
    id = Column(Integer, primary_key=True)
    cellcode = Column(Integer, nullable=False)
    cellname = Column(String(64), nullable=False)
    cellleader = Column(String(1024), nullable=False)
    cellmember = relationship("Member", backref='cellmember')
    cell_day = relationship("CellMeeting", backref='cellmetting')
    cell_plans = relationship('Plans', backref='plans')
    cell_activ = relationship('Activities', backref='activities')
    
class CellMeeting(Base):
    __tablename__='cellmetting'
    id = Column(Integer, primary_key=True)
    cmetdates = Column(Date, default=date.today())
    cmbsgrp = Column(Integer, default=0)
    cmmet = Column(String(1), default='N')
    cmoff = Column(Integer, default=0)
    cmft = Column(Integer, default=0)
    cmtotalatt = Column(Integer, default=0)
    cmseed = Column(Integer, default=0)
    cmholysprit = Column(Integer, default=0)
    cmnewcon= Column(Integer, default=0)
    cmnewcells = Column(Integer, default=0)
    cmnewbsgrp = Column(Integer, default=0)
    cell_id = Column(Integer, ForeignKey('cell.id'))

class Plans(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    prayer = Column(Text, nullable=True)
    outreach = Column(Text, nullable=True)
    visitation = Column(Text, nullable=True)
    fellowship = Column(Text, nullable=True)
    materials = Column(Text, nullable=True)
    others = Column(Text, nullable=True)
    cell_id = Column(Integer, ForeignKey('cell.id'))

class Activities(Base):
    __tablename__="activities"
    id = Column(Integer, primary_key=True)
    act_activ = Column(Text, nullable=False)
    act_date = Column(Date, default=date.today())
    cell_id = Column(Integer, ForeignKey('cell.id'))

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
