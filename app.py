from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

service_requests = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == "host":
        return redirect(url_for('host_dashboard'))
    elif username == "manager":
        return redirect(url_for('manager_dashboard'))
    else:
        return render_template('dashboard.html', username=username)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/request_service')
def request_service():
    return render_template('service_request.html')

@app.route('/submit_request', methods=['POST'])
def submit_request():
    org_name = request.form['org_name']
    cust_name = request.form['cust_name']
    role = request.form['role']
    service_needed = request.form['service_needed']
    problem_desc = request.form['problem_desc']

    service_requests.append({
        'org_name': org_name,
        'cust_name': cust_name,
        'role': role,
        'service_needed': service_needed,
        'problem_desc': problem_desc,
        'status': 'Pending'
    })

    return render_template('submission_success.html')



@app.route('/host_dashboard')
def host_dashboard():
    return render_template('host_dashboard.html', service_requests=service_requests)

@app.route('/update_status', methods=['POST'])
def update_status():
    org_name = request.form['org_name']
    action = request.form['action']

    for req in service_requests:
        if req['org_name'] == org_name:
            req['status'] = 'Accepted' if action == 'accept' else 'Rejected'
            break

    return redirect(url_for('host_dashboard'))

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('manager_dashboard.html', service_requests=service_requests)

if __name__ == '__main__':
    app.run(debug=True)
