import sys
from sqlalchemy import Column,ForeignKey,Integer,String,DateTime,desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
import sqlite3
from flask import g
from sqlalchemy.orm import sessionmaker

Base=declarative_base()

class Category(Base):
    __tablename__='category'
    name = Column(String(80),nullable=False,unique=True)
    id=Column(Integer,primary_key=True)

class Item(Base):
    __tablename__='item'
    title=Column(String(80),nullable=False,unique=True)
    id=Column(Integer,primary_key=True)
    description=Column(String(250))
    cat_id=Column(Integer,ForeignKey('category.id'))
    user=Column(String(80))
    created_date = Column(DateTime, default=datetime.utcnow)
    category=relationship(Category)
   

class CatalogItemModel():
    def __init__(self):
        database_path='sqlite:///catalog/itemcatalog.db'
        engine=create_engine(database_path)
        Base.metadata.create_all(engine)
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()
    def initialize(self):
        #session.query(CatalogItem).delete()
        #session.commit()
        # Add catalog items
        [self.session.delete(item) for item in self.get_items()]
        self.session.commit()

        [self.session.delete(item) for item in self.get_categories()]
        self.session.commit()
        
        soccer = Category(name="Soccer")
        self.session.add(soccer)
        self.session.commit()

        hockey = Category(name="Hockey")
        self.session.add(hockey)
        self.session.commit()

        shinguards = Item(category=soccer,
                          title="Shinguards",
                          description="Something for the shins",
                          user="Karl. E")
        self.session.add(shinguards)
        self.session.commit()
        stick= Item(category=hockey,
                    title="Stick",
                    description="Just a stick!",
                    user="Franz Karl")
        self.session.add(stick)
        self.session.commit()

    def get_categories(self): 
        return self.session.query(Category).all()

    def get_items(self):
        return self.session.query(Item).all()

    def get_latest_items(self,number_of_items):
        return self.session.query(Item).order_by(desc(Item.created_date)).limit(number_of_items)

    def get_items_of_category(self,category_name):
        #There must be a better way to do this...
        category = self.session.query(Category).filter_by(name=category_name).one()
        return self.session.query(Item).filter(Item.cat_id == category.id).all()

    def get_item(self,item_text):
        return self.session.query(Item).filter(Item.text == item_text).one()
