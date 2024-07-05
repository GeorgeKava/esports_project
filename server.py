from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

#write person
def write_to_file(data):
    with open('data/person.txt', 'a') as file:
        file.write(data +'\n')
        
# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Add person page
@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        country = request.form['country']
        
        data = f"{firstname}, {lastname}, {username}, {country}"
        
        write_to_file(data)
        
        return redirect(url_for('index'))
    
    return render_template('add_person.html')

# Search Person
@app.route('/search_person', methods=['GET', 'POST'])
def search_person():
    if request.method == 'POST':
        search_term = request.form['search_term'].strip().lower()
        
        results = []
        with open('data/person.txt', 'r') as file:
            for line in file:
                if search_term in line.lower():
                    results.append(line.strip().split(','))
                    
        return render_template('search_person.html', results=results, search_term=search_term)
    
    return render_template('search_person.html', results=None, search_term=None)



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)