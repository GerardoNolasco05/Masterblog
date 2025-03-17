from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_posts():
    """Load posts from the JSON file."""
    try:
        with open(os.path.join('data', 'posts.json'), 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save the posts list to the JSON file."""
    with open(os.path.join('data', 'posts.json'), 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """Render the index page with all posts."""
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle adding a new post."""
    if request.method == 'POST':
        posts = load_posts()

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_id = max([post['id'] for post in posts], default=0) + 1

        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Handle deleting a post by its ID."""
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handle updating an existing post."""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
