import os
import raildriver
from markupsafe import escape
from flask import Flask, json, request, url_for

rd = raildriver.RailDriver()
rd.set_rail_driver_connected(True)  # start data exchange
loco_name = rd.get_loco_name()
print(loco_name)

if loco_name is None:
    print("Can't find any loco")
    os._exit(1)

api = Flask(__name__)


# get a list of every controls
@api.route('/locomotive/controls', methods=['GET'])
def get_controls():
    controls = dict(rd.get_controller_list())
    return json.dumps(list(controls.values()))


@api.route('/locomotive/name', methods=['GET'])
def get_loco_name():
    text = rd.get_loco_name()
    return json.dumps(text)


@api.route('/control/<username>', methods=['GET', 'POST'])
def set_controls(username):
    global textToReturn
    print(username)
    if request.method == "GET":
        print("UwU")
        print(escape(username))
        print(rd.get_current_controller_value(username))
        textToReturn = str(rd.get_current_controller_value(username))
    else:
        print("POST")
        print(request.form["value"])
        textToReturn = rd.set_controller_value(username, float(request.form["value"]))
        if textToReturn is None:
            return

    return json.dumps(textToReturn)


if __name__ == '__main__':
    api.run()
