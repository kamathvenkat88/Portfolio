from flask import Flask, render_template
app= Flask(__name__)

@app.route('/')
def index():
	print("running");
    return render_template('index.html')