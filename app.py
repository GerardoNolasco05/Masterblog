from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


# Load posts from JSON file
def load_posts():
    try:
        with open(os.path.join('data', 'posts.json'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Store posts to JSON file
def save_posts(posts):
    with open(os.path.join('data', 'posts.json'), 'w') as file:
        json.dump(posts, file, indent=4)


posts = load_posts()  # Load posts at the start


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get the data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Create a new blog post object
        new_post = {
            'id': len(posts) + 1,  # Generate a new id
            'title': title,
            'author': author,
            'content': content
        }

        # Append to the posts list
        posts.append(new_post)

        # Save the updated posts list to the file
        save_posts(posts)

        # Redirect to home page after adding the post
        return redirect(url_for('index'))

    # If it's a GET request, render the add form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    global posts
    # Filter out the post with the given id
    posts = [post for post in posts if post['id'] != post_id]

    # Save the updated posts list to the file
    save_posts(posts)

    # Redirect back to home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        # Save the updated posts list to the file
        save_posts(posts)

        # Redirect to the index page
        return redirect(url_for('index'))

    # For GET request, display the form pre-filled with the post's details
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
