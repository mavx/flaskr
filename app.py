from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user = {'nickname': 'MavX'}
    return render_template(
        'index.html',
        title='Home',
        user=user
    )

@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
