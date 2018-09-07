
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
category1 = Category(name="Curry")

session.add(category1)
session.commit()

recipe1 = Recipe(name="Red Curry", description="Red curry is a popular Thai dish consisting of red curry paste cooked in coconut milk with meat added, such as chicken, beef, pork, duck or shrimp, or vegetarian protein source such as tofu.",
                      category=category1)

session.add(recipe1)
session.commit()


recipe2 = Recipe(name="Chicken tikka masala", description="The sauce is usually creamy and orange-coloured.",
                     category=category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name="Chickin curry", description="curry with chickin",
                    category=category1)

session.add(recipe3)
session.commit()


# Menu for Super Stir Fry
category2 = Category(name="Pizza")

session.add(category2)
session.commit()


recipe1 = Recipe(name="Margherita", description="Pizza Margherita is a typical Neapolitan pizza, made with San Marzano tomatoes, mozzarella fior di latte,[1] fresh basil, salt and extra-virgin olive oil.",
                      category=category2)

session.add(recipe1)
session.commit()


print "added menu items!"
