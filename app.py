from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/python.html')
def python():
    return render_template('python.html')

@app.route('/docker.html')
def docker():
    return render_template('docker.html')

@app.route('/jenkins.html')
def jenkins():
    return render_template('jenkins.html')

@app.route('/kubernetes.html')
def kubernetes():
    return render_template('kubernetes.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
