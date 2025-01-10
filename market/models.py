from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default=500)
    item = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        s = str(self.budget)
        count = 0
        result = ''
        for i in range(len(s)-1, -1, -1):  
            if count == 3:
                result += ','  
                count = 0
            result += s[i]
            count += 1

        result = result[::-1]
        return '$'+result

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_password_text):
        self.password_hash = bcrypt.generate_password_hash(plain_password_text).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'
