#!flask/bin/python3
import json
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'
    #return render_template('/home/anna/API/templates/index.html')

infa = {
    'count_members': 0,
    'count_projects': 0,
    'count_events': 0

}


@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(infa['count_members'])


@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify(infa['count_projects'])


@app.route('/events', methods=['GET'])
def get_events():

    return jsonify(infa['count_events'])



@app.route('/members/<int:new>', methods=['POST', 'GET'])
def UpdateMembers(new):

    infa['count_members'] = new
    return jsonify(infa)


@app.route('/projects/<int:new>', methods=['POST', 'GET'])
def UpdateProjects(new):

    infa['count_projects'] = new

    return jsonify(infa)


@app.route('/events/<int:new>', methods=['POST', 'GET'])
def update(new):

    infa['count_events'] = new

    return jsonify(infa)



if __name__ == "__main__":
    app.run()
