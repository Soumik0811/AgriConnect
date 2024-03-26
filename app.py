##setup flask app
from flask import Flask, render_template, request, redirect, url_for,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
from supabase import supabase
from dealers import fun
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

##set home route
@app.route('/')
def home():
    return ("home page")

@app.route('/auth/<authtype>')
def auth(authtype):
    return render_template('auth.html',authtype=authtype)

@app.route('/login', methods=['POST'])
def login():
    # Get the form data from the request
    phone = request.form['phone']
    password = request.form['password']

    # Perform authentication (replace this with your actual authentication logic)
    data= supabase.table('farmers').select('*').eq('phone', phone).execute()
    user = data['data'][0]
    if user:
        if check_password_hash(user['password'], password):
            session['name']  = user['name']
            session['phone'] = user['phone']
            return redirect(url_for('profile'))
        else:
            return ("invalid password")
    else:
        return "User not found"
                
                         
@app.route('/register', methods=['POST'])
def register():
    # Get the form data from the request
    name = request.form["name"]
    data= supabase.table('farmers').select('*').eq('phone', phone).execute()
    user = data['data'][0]
    if user:
        return "This number is already registered.";
    phone = request.form['phone']
    password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
    
    # Insert data into the 'farmers' table
    data = supabase.table('farmers').insert({"name": name, "phone": phone,"password": password}).execute()
    
    return (f"{data}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth',authtype='login'))
    ##empty session and redirect to login



import geocoder
@app.route('/profile')
def profile():
    if 'phone' in session:
       return render_template("middle.html")
    else:
        return redirect(url_for('auth',authtype='login'))
    
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    ##if phone does not exist in session redirect to login
    if 'phone' not in session:
        return redirect(url_for('auth',authtype='login'))
    if request.method == 'POST':
        session['crop'] = request.form["crop"]
        # Process the crop data (e.g., save to database, perform calculations, etc.)
        return redirect(url_for('dashboard'))
    return render_template("ask.html")

from npk import recommend
@app.route('/dashboard')
def dashboard():
    while True:  # Keep looping until no error is thrown
        try:
            g = geocoder.ip('me')
            address = g.geojson
            address1 = address['features'][0]['properties']['state']
            prompt = f"seed dealers in hyderabad"
            output = fun({
                "question": prompt,
            })
            print(session['crop'])
            npk = recommend({
                "question": session['crop']
            })
            if 'phone' not in session:
                return redirect(url_for('auth', authtype='login'))
            return render_template('dashboard.html', name=session['name'], address=address['features'][0]['properties']['address'], output=output, npk=npk)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)