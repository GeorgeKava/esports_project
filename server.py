from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

#read file
def read_file():
    results = []
    with open('data/person.txt', 'r') as file:
        for line in file:
            person = line.strip().split(',')
            results.append({
                'id': person[0],
                'firstname': person[1],
                'lastname': person[2],
                'username': person[3],
                'country': person[4]
            })
    return results

#write person
def write_to_file(results):
    with open('data/person.txt', 'w') as file:
        for person in results:
            file.write(f"{person['id']},{person['firstname']},{person['lastname']},{person['username']},{person['country']}\n")
        
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
        
        results = read_file()
        id = str(len(results) + 1)
        results.append({
            'id': id,
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'country': country
        })
        write_to_file(results)
        return redirect(url_for('index'))
    
    return render_template('add_person.html')

# Search Person
@app.route('/search_person', methods=['GET', 'POST'])
def search_person():
    if request.method == 'POST':
        search_term = request.form['search_term'].strip().lower()
        results = read_file()
        search_results = [person for person in results if search_term in person['firstname'].lower() or
                                                            search_term in person['lastname'].lower() or
                                                            search_term in person['username'].lower() or 
                                                            search_term in person['country'].lower()]
        return render_template('search_person.html', results=search_results, search_term=search_term)
    return render_template('search_person.html', results=None, search_term=None)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_person(id):
    results = read_file()
    persons = next((person for person in results if person['id'] == str(id)), None)
    if persons:
        if request.method == 'POST':
            persons['firstname'] = request.form['firstname']
            persons['lastname'] = request.form['lastname']
            persons['username'] = request.form['username']
            persons['country'] = request.form['country']
            write_to_file(results)
            return redirect(url_for('index'))
        return render_template('update_person.html', persons = persons)
    return 'Person not found', 404

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_person(id):
    results = read_file()
    results = [person for person in results if person['id'] != str(id)]
    write_to_file(results)
    return redirect(url_for('index'))

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)