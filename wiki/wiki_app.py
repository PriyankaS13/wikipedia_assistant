import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('app.log')
logger.addHandler(fh)

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class OutdatedPageList(db.Model):
    __tablename__ = 'outdated_page_list'
    category = db.Column(db.String(4000))
    outdated_page_id = db.Column(db.Integer, primary_key=True)

    def __str__(self):
        return {'category': self.category, 'outdated_page_id': self.outdated_page_id}


def serialize_raw_query(row):
    logger.info("serializing raw sql query output")
    if not row:
        return
    d = {}
    for column, value in row.items():
        d[column] = str(value)
    return d


@app.route('/api/v1/rawquery',  methods=['POST'])
def execute_raw_sql_query():
    '''
    Post call that accepts query in body and provides query output as  response
    :return:
    '''
    sql_injection = ["DELETE", "TRUNCATE", "DROP", "UPDATE", "INSERT", "CREATE"]
    if request.json:
        content = request.json
        sql = content['query']
        logger.debug("checking for sql injection in raw query")
        sql_injection_check = [inj in sql.upper() for inj in sql_injection]
        if any(sql_injection_check):
            logger.debug("sql injection detected sending error response")
            return jsonify({"query": sql, "error": "Not a readonly query"}), 400
        try:
            results = db.engine.execute(text(sql))
        except Exception as e:
            logger.error(f"Error executing sql query {e.args}")
            return jsonify({"error": "invalid sql query"}), 400
        response = {}
        for row in results:
            response.update(serialize_raw_query(row))
        return jsonify(response), 200
    else:
        return jsonify({"error": "Empty request body"}), 400


@app.route('/api/v1/outdatedpages', methods=['GET'])
def get_outdated_pages():
    '''
    Get call which gives most outdated pages for a category.

    :return:
    '''
    args = request.args
    try:
        if "category_name" in args:
            all_results = OutdatedPageList.query.filter_by(category=args['category_name']).all()
        else:
            all_results = OutdatedPageList.query.all()
    except Exception as e:
        logger.error(f"Error retriving data for outdated pagelist: {e.args}")
        return jsonify({"error": f"couldn't retrieve result: {e.args}"}), 400
    response = [{'category': row.category, 'outdated_page_id': row.outdated_page_id} for row in all_results]
    return jsonify(response), 200


if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=False, port=8000)