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
   
    master ={} 
    cat = map(os.path.basename,filter(os.path.isdir,glob.glob('nightly_results/{0}/*'.format(date))))
    for c in cat:
        master[c] = {}
        analyses = filter(os.path.isdir, glob.glob('nightly_results/{0}/{1}/plots/*'.format(date,c)))
        analyses = [x.rsplit("/",1)[-1] for x in analyses]
        for a in analyses:
	    plotlist = [os.path.basename(p).rsplit('.',1)[0] for p in glob.glob('nightly_results/{0}/{1}/plots/{2}/*.dat'.format(date,c,a))]
            master[c][a] = plotlist
            
       
#    analyses = map(os.path.basename,filter(os.path.isdir,glob.glob('nightly_results/{0}/*'.format(date))))
#    plotlists = [[os.path.basename(p).rsplit('.',1)[0] for p in glob.glob('nightly_results/{0}/{1}/plots/*.dat'.format(date,a))] for a in analyses]
#    plotdata = dict(zip(analyses,plotlists))
    return flask.render_template('result.html',date = date, plotdata = master)
    
@app.route('/plot/<date>/<cat>/<analysis>/<path:file>')
def plots(date,cat,analysis,file):
  resultdir = 'nightly_results/{0}/{1}/plots/{2}'.format(date,cat,analysis)
  return flask.send_from_directory(resultdir,file)

@app.route('/catfile/<date>/<cat>/<path:file>')
def catfile(date, cat, file):
  resultdir = 'nightly_results/{0}/{1}'.format(date,cat)
  return flask.send_from_directory(resultdir, file)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000)
