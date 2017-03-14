from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import queryRestaurants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem


# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class requestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				restaurant = session.query(Restaurant).all()
				output=""
				output += "<html><body>"
				output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
				for rest in restaurant:
					output += rest.name
					output +="</br>"
					output +="<a href='/restaurants/%s/edit'>Edit</a>"%rest.id
					output +="</br>"
					output +="<a href='/restaurants/%s/delete'>Delete</a><br>"%rest.id
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/edit"):
				restId = self.path.split("/")[2]
				restaurantID = session.query(Restaurant).filter_by(id=restId).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Edit %s's name</h1>"%restaurantID.name
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" %restId
				output += "<input name = 'editRestaurantName' type = 'text' placeholder = '%s' > "%restaurantID.name
				output += "<input type='submit' value='Rename'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/delete"):
				restId = self.path.split("/")[2]
				restaurantID = session.query(Restaurant).filter_by(id=restId).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure you want to delete %s</h1>"%restaurantID.name
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" %restId
				output += "<input type='submit' value='Delete'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				print output
				return	

		except IOError:
			self.send_error((404, 'File Not Found: %s' % self.path))



	def do_POST(self):
			try:
				if self.path.endswith("/restaurants/new"):
					ctype, pdict = cgi.parse_header(
						self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)
						messagecontent = fields.get('newRestaurantName')
						newRestaurant = Restaurant(name=messagecontent[0])
						session.add(newRestaurant)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()
				if self.path.endswith("/edit"):
					ctype, pdict = cgi.parse_header(
						self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)
						messagecontent = fields.get('editRestaurantName')
						restId = self.path.split("/")[2]
						rest = session.query(Restaurant).filter_by(id=restId).one()
						if rest != []:
							rest.name=messagecontent[0]
							session.add(rest)
							session.commit()
							self.send_response(301)
							self.send_header('Content-type', 'text/html')
							self.send_header('Location', '/restaurants')
							self.end_headers()
				if self.path.endswith("/delete"):
					ctype, pdict = cgi.parse_header(
						self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)
						restId = self.path.split("/")[2]
						rest = session.query(Restaurant).filter_by(id=restId).one()
						if rest != []:
							session.delete(rest)
							session.commit()
							self.send_response(301)
							self.send_header('Content-type', 'text/html')
							self.send_header('Location', '/restaurants')
							self.end_headers()
					
			except:
				pass


def main():
	try:
		port = 8080
		server = HTTPServer(('',port),requestHandler)
		print "The server is running on %s .." %port
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C Key is entered to stop server"
		server.socket.close()		

if __name__ == '__main__':
	main()