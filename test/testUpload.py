import os
from flask import Blueprint, jsonify, request, flash, redirect
from werkzeug.utils import secure_filename
from flask import Flask
from logging import getLogger

logger=getLogger()

dangqian=os.path.dirname(os.path.dirname(__file__))

UPLOAD_PATH=dangqian+'/uploads/static/'

ALLOWED_EXTENSIONS = ['xls', 'xlsx','csv']

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})

        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            logger.debug('No selected file')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    logger.debug('filename is %s' % origin_file_name)
                    # filename = secure_filename(file.filename)
                    filename = origin_file_name

                    if os.path.exists(UPLOAD_PATH):
                        logger.debug('%s path exist' % UPLOAD_PATH)
                        pass
                    else:
                        logger.debug('%s path not exist, do make dir' % UPLOAD_PATH)
                        os.makedirs(UPLOAD_PATH)
                    print(UPLOAD_PATH)
                    file.save(os.path.join(UPLOAD_PATH, filename))
                    print(file)
                    logger.debug('%s save successfully' % filename)
                    return jsonify({'code': 0, 'filename': origin_file_name, 'msg': ''})
                else:
                    logger.debug('%s not allowed' % file.filename)
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                logger.debug('upload file exception: %s' % e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})

@app.route('/delete', methods=['GET','POST'])
def delete_file():
    if request.method == 'GET':
        filenames = request.args.get('filename')
        print(filenames)
        #timestamp = request.args.get('timestamp')
        #logger.debug('delete file : %s, timestamp is %s' % (filename, timestamp))
        try:
            fullfile = os.path.join(UPLOAD_PATH, filenames)

            if os.path.exists(fullfile):
                os.remove(fullfile)
                logger.debug("%s removed successfully" % fullfile)
                return jsonify({'code': 0, 'msg': ''})
            else:
                return jsonify({'code': -1, 'msg': 'File not exist'})

        except Exception as e:
            logger.debug("delete file error %s" % e)
            return jsonify({'code': -1, 'msg': 'File deleted error'})

    else:
        return jsonify({'code': -1, 'msg': 'Method not allowed'})

if __name__ == '__main__':
    app.run(debug=True)