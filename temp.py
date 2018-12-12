from Users import User

User.initializeConnectionPool()
user = User('nitsats@gmail.com', 'Satish', 'Kumar')
print(user)
user.save_to_db()
user = User.load_from_db('nitsats@gmail.com')
print(user)
            