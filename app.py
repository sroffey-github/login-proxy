from flask import Flask, render_template, request, flash, session
import controller, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usern = request.form['username']
        passwd = request.form['password']
        if controller.authenticate(usern, passwd):
            session['logged_in'] = usern
        else:
            flash('Invalid username or password')
            return render_template('index.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    controller.init()
    app.run(debug=True)