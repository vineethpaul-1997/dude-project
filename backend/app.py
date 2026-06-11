from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "application": "Python DevOps Backend",
        "status": "Running"
    })

@app.route('/python')
def python():
    return jsonify({
        "title": "Python",
        "subtitle": "Backend Service",
        "description": "Python is used for web development, AI, automation and DevOps."
    })

@app.route('/docker')
def docker():
    return jsonify({
        "title": "Docker",
        "subtitle": "Containerized",
        "description": "Docker packages applications into lightweight containers."
    })

@app.route('/jenkins')
def jenkins():
    return jsonify({
        "title": "Jenkins",
        "subtitle": "CI/CD Pipeline",
        "description": "Jenkins automates build, testing and deployment."
    })

@app.route('/kubernetes')
def kubernetes():
    return jsonify({
        "title": "Kubernetes",
        "subtitle": "Orchestrated",
        "description": "Kubernetes manages containerized applications."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
