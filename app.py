from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/postgres'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'game_history_database'}
    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    startdate = db.Column(db.Date)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Game_Developer(db.Model):
    __tablename__ = 'game_developer'
    __table_args__ = {'schema': 'game_history_database'}
    enterprise_name = db.Column(db.String(30), primary_key=True)
    location = db.Column(db.String(50))
    num_employees = db.Column(db.Integer)
    is_indie = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Game(db.Model):
    __tablename__ = 'game'
    __table_args__ = {'schema': 'game_history_database'}
    game_name = db.Column(db.String(255), primary_key=True)
    gdev = db.Column(db.String(50), db.ForeignKey('game_history_database.game_developer.enterprise_name'))
    genre = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    is_multiplayer = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Plays(db.Model):
    __tablename__ = 'plays'
    __table_args__ = {'schema': 'game_history_database'}
    username = db.Column(db.String(30), db.ForeignKey('game_history_database.user.UserName'), primary_key=True)
    game_name = db.Column(db.String(255), db.ForeignKey('game_history_database.game.Game_Name'), primary_key=True)
    hours = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        users_dict = [user.as_dict() for user in users]
        return jsonify({'users': users_dict})
    elif request.method == 'POST':
        new_user_data = request.json
        new_user = User(**new_user_data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

@app.route('/developers', methods=['GET', 'POST'])
def handle_developers():
    if request.method == 'GET':
        developers = Game_Developer.query.all()
        developers_dict = [dev.as_dict() for dev in developers]
        return jsonify({'developers': developers_dict})
    elif request.method == 'POST':
        new_developer_data = request.json
        new_developer = Game_Developer(**new_developer_data)
        db.session.add(new_developer)
        db.session.commit()
        return jsonify({'message': 'Game Developer created successfully'}), 201

@app.route('/developers/<enterprise_name>', methods=['GET'])
def get_developer(enterprise_name):
    developer = Game_Developer.query.get(enterprise_name)
    if developer:
        return jsonify(developer.as_dict())
    else:
        return jsonify({'error': 'Game Developer not found'}), 404

@app.route('/games', methods=['GET', 'POST'])
def handle_games():
    if request.method == 'GET':
        games = Game.query.all()
        games_dict = [game.as_dict() for game in games]
        return jsonify({'games': games_dict})
    elif request.method == 'POST':
        new_game_data = request.json
        new_game = Game(**new_game_data)
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game created successfully'}), 201

@app.route('/games/<game_name>', methods=['GET'])
def get_game(game_name):
    game = Game.query.get(game_name)
    if game:
        return jsonify(game.as_dict())
    else:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/plays', methods=['GET', 'POST'])
def handle_plays():
    if request.method == 'GET':
        plays = Plays.query.all()
        plays_dict = [play.as_dict() for play in plays]
        return jsonify({'plays': plays_dict})
    elif request.method == 'POST':
        new_play_data = request.json
        new_play = Plays(**new_play_data)
        db.session.add(new_play)
        db.session.commit()
        return jsonify({'message': 'Play record created successfully'}), 201

@app.route('/plays/<username>/<game_name>', methods=['GET'])
def get_play(username, game_name):
    play = Plays.query.get((username, game_name))
    if play:
        return jsonify(play.as_dict())
    else:
        return jsonify({'error': 'Play record not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
