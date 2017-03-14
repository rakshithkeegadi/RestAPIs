from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app= Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])
	
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menuItems = session.query(MenuItem).order_by(MenuItem.name).filter_by(restaurant_id=restaurant.id).all()
	return render_template('menu.html',restaurants=restaurant,items=menuItems, restaurant_id=restaurant_id)

@app.route('/')	
@app.route('/restaurants/')	
def restaurants():
	restaurant=session.query(Restaurant).all()
	return render_template('restaurant.html',restaurant=restaurant)
	
@app.route('/restaurants/<int:restaurant_id>/new/',methods=['GET','POST'])

def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("Menu item created!")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id=restaurant_id)

@app.route('/restaurants/newRestaurant/',methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant= Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("Menu item created!")
		return redirect('http://localhost:5000/restaurants/')
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])	
def editMenuItem(restaurant_id, menu_id):
	editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name=request.form['name']
		if request.form['price']:
			editedItem.price=request.form['price']
		session.add(editedItem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id, i=editedItem)

@app.route('/restaurants/<int:restaurant_id>/edit/',methods=['GET','POST'])	
def editRestaurantItem(restaurant_id):
	editedItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name=request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Restaurant item edited!")
		return redirect('http://localhost:5000/restaurants/')
	else:
		return render_template('editrestaurantitem.html',restaurant_id=restaurant_id, name=editedItem)
		

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])	
def deleteMenuItem(restaurant_id, menu_id):
	deleteItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method =='POST':
		session.delete(deleteItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html',restaurant_id=deleteItem.restaurant_id,item = deleteItem)
		
@app.route('/restaurants/<int:restaurant_id>/delete/',methods=['GET','POST'])			
def deleteRestaurantItem(restaurant_id):
	deleteItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method =='POST':
		session.delete(deleteItem)
		session.commit()
		flash("Restaurant item deleted!")
		return redirect('http://localhost:5000/restaurants/')
	else:
		return render_template('deleterestaurant.html',restaurant_id=deleteItem.id, name = deleteItem)		

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)