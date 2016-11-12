from gcloud import datastore 
import datetime

client= datastore.Client()

def add_user(name,passwort,email):
    key = client.key('User')
    user = datastore.Entity(key)
    user.update({
        'created': datetime.datetime.utcnow(),
        'name': name,
        'password': passwort,
        'email': email
    })
    client.put(user)
    return  user.key

def get_user(name,password):
    query = client.query(kind='User')
    query.add_filter('name', '=', name)
    query.add_filter('password', '=', password)
    query=list(query.fetch())
    return query

def add_new_post(subject, content):
    key = client.key('Blog')
    blog = datastore.Entity(key)
    blog.update({
        'created': datetime.datetime.utcnow(),
        'subject': subject,
        'content': content
    })
    client.put(blog)
    return  blog.key

def get_list_of_blog_posts():
    query = client.query(kind='Blog')
    query.order = ['created']
    return list(query.fetch())

def get_post(id):
    key = client.key('Blog', id)
    blog = client.get(key)
    return blog