import flask
app = flask.Flask(__name__)


app.debug = True

import glob
import os

@app.route('/')
def home():
    result_folders = glob.glob('nightly_results/*')
    just_dates = [s.split('/',1)[-1] for s in glob.glob('nightly_results/*')]
    return flask.render_template('home.html',results = just_dates)
        
@app.route('/result/<date>')
def result_view(date):
    
    analyses = map(os.path.basename,filter(os.path.isdir,glob.glob('nightly_results/{}/*'.format(date))))
    plotdata = {a:[os.path.basename(p).rsplit('.',1)[0] for p in glob.glob('nightly_results/{}/{}/*.dat'.format(date,a))] for a in analyses}
    return flask.render_template('result.html',date = date, plotdata = plotdata)
    
@app.route('/plot/<date>/<analysis>/<path:file>')
def plots(date,analysis,file):
  resultdir = 'nightly_results/{}/{}'.format(date,analysis)
  print resultdir
  return flask.send_from_directory(resultdir,file)


if __name__ == "__main__":
    app.run()