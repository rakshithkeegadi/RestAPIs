from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
import datetime
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def getRestaurants():
	restaurants = session.query(Restaurant).all()
	return restaurants
def getRestaurantbyId(id):
	restaurant = session.query(Restaurant).get(id)
	return
def addNewRestaurant(restaurantName):
	restaurant = Restaurant(name = restaurantName)
	session.add(restaurant)
	session.commit()