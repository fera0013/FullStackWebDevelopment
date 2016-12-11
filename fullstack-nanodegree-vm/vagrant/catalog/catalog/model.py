import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
import sqlite3
from flask import g
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'item'
    title = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    created_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'id': self.id,
            'description': self.description,
            'cat_id': self.cat_id}


class CatalogItemModel():
    def __init__(self):
        database_path = 'sqlite:///catalog/itemcatalog.db'
        engine = create_engine(database_path)
        Base.metadata.create_all(engine)
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_categories(self):
        """
        get_categories: returns a list with all categories
        Args:
            None
        Returns:
            list of Category objects
        """
        return self.session.query(Category).all()

    def get_category(self, name):
        """
        get_category: Returns the Category object with name==name
        Args:
            name (data type: str): The categorie's name
        Returns:
            Category object
        """
        return self.session.query(Category).filter_by(name=name).one()

    def get_latest_items(self, number_of_items):
        """
        get_latest_items: Returns the most recently added items
        Args:
            number_of_items (data type: int): The number of most recent items
        Returns:
            List of Item objects
        """

        return self.session.query(Item).\
            order_by(desc(Item.created_date)).limit(number_of_items)

    def get_items_of_category(self, category_name):
        """
        get_latest_items: Returns all items of a specific category
        Args:
            category_name (data type: str): The categorie's name
        Returns:
            List of Item objects
        """
        category = self.session.query(Category).\
            filter_by(name=category_name).one()
        return self.session.query(Item).\
            filter(Item.cat_id == category.id).all()

    def get_item(self, item_title):
        """
        get_latest_items: Returns a specific item
        Args:
            item_title (data type: str): The item's title
        Returns:
            An item object
        """
        return self.session.query(Item).filter(Item.title == item_title).one()

    def add_item(self, item):
        """
        add_item: Adds or updates a database object
        Args:
            item (data type: Base): A Category,Item or User object
        Returns:
            The added or updated item
        """
        self.session.add(item)
        self.session.commit()
        return item

    def delete_item(self, item):
        """
        delete_item: Deletes a database object
        Args:
            item (data type: Base): A Category,Item or User object
        Returns:
            None
        """
        self.session.delete(item)
        self.session.commit()

    # ToDo: Verify email_address format
    def add_user(self, email_address):
        """
        add_user: Returns the user with email_address or adds a new one
        if this user does not exist
        Args:
            email_address (data type: str): The email_address of a user
        Returns:
            A User object
        """
        user = self.session.query(User).\
            filter(User.email == email_address).all()
        if len(user) > 0:
            return user[0]
        user = User(email=email_address)
        self.session.add(user)
        self.session.commit()
        return user