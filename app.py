from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Extract data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Load existing posts from the JSON file
        with open(os.path.join('data', 'posts.json')) as file:
            blog_posts = json.load(file)

        # Generate a new ID based on the last post's ID
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        # Create the new post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add the new post to the list
        blog_posts.append(new_post)

        # Save the updated posts list back to the JSON file
        with open(os.path.join('data', 'posts.json'), 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template('add.html')
