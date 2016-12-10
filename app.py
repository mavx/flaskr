from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user = {'nickname': 'MavX'}
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )

@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
