from flask import Flask, send_from_directory
app= Flask(__name__, template_folder="./")

@app.route('/')
def index():
	return send_from_directory('./', 'index.html')

if __name__ == '__main__':
	app.run(threaded=True, port=33507)
