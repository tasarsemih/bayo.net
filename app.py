from flask import Flask, render_template, request, redirect, url_for
import random, string, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    cvs = []
    try:
        import sqlite3
        conn = sqlite3.connect('cv.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS cvs (id INTEGER PRIMARY KEY, name TEXT, filename TEXT, link TEXT)')
        c.execute('SELECT * FROM cvs')
        cvs = c.fetchall()
        conn.close()
    except:
        cvs = []
    return render_template('index.html', cvs=cvs)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        file = request.files.get('file')
        link = request.form.get('link')
        if file and name:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            try:
                import sqlite3
                conn = sqlite3.connect('cv.db')
                c = conn.cursor()
                c.execute('INSERT INTO cvs (name, filename, link) VALUES (?, ?, ?)', (name, file.filename, link))
                conn.commit()
                conn.close()
            except Exception as e:
                print("DB hatası:", e)
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        terms = request.form['terms']
        score = random.randint(100, 1000)
        domains = [''.join(random.choices(string.ascii_lowercase+string.digits, k=16))+".onion" for _ in range(5)]
        risk = random.choice(["LOW", "MEDIUM", "HIGH"])
        return render_template('scan.html', terms=terms, score=score, domains=domains, risk=risk)
    return render_template('scan.html')

if __name__ == '__main__':
    app.run(debug=True)
