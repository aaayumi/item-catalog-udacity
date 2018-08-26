
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Recipe

engine = create_engine('sqlite:///category.db')
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
session = DBSession()


# Menu for UrbanBurger
category1 = Category(name="Urban Burger")

session.add(category1)
session.commit()

recipe1 = Recipe(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.50", course="Entree", category=category1)

session.add(recipe1)
session.commit()


recipe2 = Recipe(name="French Fries", description="with garlic and parmesan",
                     price="$2.99", course="Appetizer", category=category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name="Chicken Burger", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                     price="$5.50", course="Entree", category=category1)

session.add(recipe3)
session.commit()


# Menu for Super Stir Fry
category2 = Category(name="Super Stir Fry")

session.add(category2)
session.commit()


recipe1 = Recipe(name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
                     price="$7.99", course="Entree", category=category2)

session.add(recipe1)
session.commit()


print "added menu items!"
