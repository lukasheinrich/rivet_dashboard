import flask
app = flask.Flask(__name__)


app.debug = True

import glob

@app.route('/')
def home():
    result_folders = glob.glob('nightly_results/*')
    just_dates = [s.split('/',1)[-1] for s in glob.glob('nightly_results/*')]
    return flask.render_template('home.html',results = just_dates)
        
@app.route('/result/<date>')
def result_view(date):
    return flask.render_template('result.html',date = date)
    
@app.route('/plot/<date>/<path:file>')
def plots(date,file):
  resultdir = 'nightly_results/{}/MC_GENERIC'.format(date)
  print resultdir
  return flask.send_from_directory(resultdir,file)


if __name__ == "__main__":
    app.run()