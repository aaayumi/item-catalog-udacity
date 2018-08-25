from squalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Recipe

engine = create_engine('sqlite:///recipe.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Category Curry
category1 = Category(name="Curry")

session.add(category1)
session.commit()

recipe1 = Recipe(name="Chicken Curry", description="Curry with chicken", difficulty="low", Category=category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name="Red Curry", description="Thai red curry", difficulty="medium", Category=category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name="Vegetable curry", description="Curry with a lot of vegetables ", difficulty="low", Category=category1)

session.add(recipe3)
session.commit()

#Category Pizza
category2 = Category(name="Pizza")

session.add(category2)
session.commit()

recipe1 = Recipe(name="Margerita", description="Tomate and mozzarela cheese", difficulty="low", Category=category2)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name="Four cheese", description="Pizza with four different kinds of cheese", difficulty="medium", Category=category2)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name="Salami pizza", description="Pizza with full of samali", difficulty="low", Category=category2)

session.add(recipe3)
session.commit()

print "Add recipes"
