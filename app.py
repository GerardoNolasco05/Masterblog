from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Open the posts.json file in the 'data' folder
    with open(os.path.join('data', 'posts.json')) as file:
        blog_posts = json.load(file)  # Load the posts data from JSON file

    # Pass the 'blog_posts' to the template
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
