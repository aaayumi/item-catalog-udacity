from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Recipe, User

engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name='Ayumi Saito',email='ayumi@gmail.com' )
session.add(user1)
session.commit()

category1 = Category(name="Curry")

session.add(category1)
session.commit()

recipe1 = Recipe(name="Red Curry",
                 description="Red curry is a popular Thai dish consisting of red curry paste cooked in coconut milk"
                             " with meat added, such as chicken, beef, pork, duck or shrimp, or vegetarian protein "
                             "source such as tofu.",
                 category=category1, user=user1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name="Chicken tikka masala", description="The sauce is usually creamy and orange-coloured.",
                 category=category1, user=user1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name="Chickin curry", description="curry with chickin",
                 category=category1, user=user1)

session.add(recipe3)
session.commit()

category2 = Category(name="Pizza")

session.add(category2)
session.commit()

recipe1 = Recipe(name="Margherita",
                 description="Pizza Margherita is a typical Neapolitan pizza, made with San Marzano tomatoes, "
                             "mozzarella fior di latte,[1] fresh basil, salt and extra-virgin olive oil.",
                 category=category2, user=user1)

session.add(recipe1)
session.commit()

print "categories and recipes are added!"
