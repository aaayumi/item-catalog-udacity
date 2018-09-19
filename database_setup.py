import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """User data
      Returns:
          user_id,
          user_name,
          user_email
          """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Category(Base):
    """Category data
      Returns:
         category_id,
         category_name
          """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Recipe(Base):
    """Recipe data
       Returns:
          recipe_name,
          recipe_id,
          recipe_description,
          category_id
           """
    __tablename__ = 'recipe'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, backref=backref('recipe', cascade="all, delete-orphan"))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///category.db')

Base.metadata.create_all(engine)
