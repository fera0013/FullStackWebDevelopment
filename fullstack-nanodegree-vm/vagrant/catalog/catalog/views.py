"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,url_for, request,redirect,flash,jsonify,make_response
from catalog import app
import model
from flask import session as login_session
import random,string
import model 
import httplib2
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import requests

db = model.CatalogItemModel()
#db.initialize()
state=''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
app.secret_key=state

# Create anti-forgery state token
@app.route('/login')
def Login():
    login_session['state'] = app.secret_key
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('catalog/client_secrets.json', scope='',redirect_uri='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    CLIENT_ID = json.loads(
    open('catalog/client_secrets.json', 'r').read())['web']['client_id']
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(request.host_url)
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    categories=db.get_categories()
    latest_items=db.get_latest_items(2)
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        categories=categories,
        latest_items=latest_items,
        logged_in='username' in login_session
    )


@app.route('/catalog/<string:category_name>/items', methods=['GET', 'POST'])
def Catalog(category_name):
    categories=db.get_categories()
    items=db.get_items_of_category(category_name)
    return render_template('catalog.html',
                           categories=categories, 
                           items=items,
                           logged_in='username' in login_session)

@app.route('/catalog/<string:category_name>/<string:item_title>', methods=['GET', 'POST'])
def Item(category_name,item_title):
    item=db.get_item(item_title)
    logged_in='username' in login_session
    authorized=('email' in login_session and item.user.email==login_session['email'])
    return render_template('item.html', 
                           item=item,
                           logged_in=logged_in,
                           authorized=authorized)

@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
def Edit(item_title):
    item=db.get_item(item_title)
    categories=db.get_categories()
    if request.method == 'GET':
        return render_template('edit.html',
                               categories=categories, 
                               item=item,
                               route=url_for('Edit',item_title=item.title))
    else:
        if request.form['title']:
            item.text = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            category_name=request.form['category']
            category=db.get_category(category_name)
            item.category=category
        db.add_item(item)
        return redirect(url_for('home'))

@app.route('/catalog/add', methods=['GET', 'POST'])
def Add():
    if 'email' in login_session:
        user_mail=login_session['email']
    else:
        return redirect(url_for('home'))
    user=db.add_user(user_mail)
    categories=db.get_categories()
    item=model.Item(title='new item',category=categories[0],user= user)
    if request.method == 'GET':
        return render_template('edit.html',
                               categories=categories, 
                               item=item,
                               route=url_for('Add',item_title=item.title))
    else:
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            category_name=request.form['category']
            category=db.get_category(category_name)
            item.category=category
        db.add_item(item)
        return redirect(url_for('home'))

@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
def Delete(item_title):
    item=db.get_item(item_title)
    if request.method == 'GET':
        return render_template('delete.html', 
                               item=item,
                               logged_in='username' in login_session)
    else:
        db.delete_item(item)
        return redirect(url_for('home'))

@app.route('/catalog/<string:category_name>/json')
def CategoryJson(category_name):
    category=db.get_category(category_name)
    serialized_category = category.serialize
    items=db.get_items_of_category(category.name)
    serializedItems = []
    for item in items:
        serializedItems.append(item.serialize)
    serialized_category['items'] = serializedItems
    return jsonify(category=serialized_category)

@app.route('/catalog/<string:category_name>/<string:item_name>/json')
def ItemJson(category_name,item_name):
    item=db.get_item(item_name)
    return jsonify(item=item.serialize)
