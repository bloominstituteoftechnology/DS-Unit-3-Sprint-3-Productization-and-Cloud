from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# class City(DB.Model):
# 	id = DB.Column(DB.Integer, primary_key=True)
# 	city = DB.Column(DB.String(30), nullable=False)
#
# 	def __repr__(self):
# 		return '<City {}>'.format(self.city)
#
# class parameter(DB.Model):
# 	id = DB.Column(DB.BigInteger, primary_key=True)
# 	text = DB.Column(DB.Unicode(500), nullable=False)
#
# 	def __repr__(self):
# 		return '<Parameter {}>'.format(self.parameter)