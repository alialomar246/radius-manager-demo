from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
app.permanent_session_lifetime = timedelta(minutes=30)

admins = {
    "admin": "1234",
    "manager": "managerpass"
}

users = [
    {"username": "user1", "package": "Basic", "ip": "192.168.1.100", "active": True},
    {"username": "user2", "package": "Premium", "ip": "192.168.1.101", "active": False}
]

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in admins and admins[username] == password:
            session.permanent = True
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('تم تسجيل الخروج', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    total_users = len(users)
    online_users = sum(1 for u in users if u["active"])
    expired_users = sum(1 for u in users if not u["active"])
    return render_template('dashboard.html',
                           username=session['user'],
                           total_users=total_users,
                           online_users=online_users,
                           expired_users=expired_users,
                           users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)