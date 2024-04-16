from flask import Flask, jsonify
from src.blueprints.entrenamiento import entrenamientos_blueprint
from src.errors.errors import ApiError
from flask_cors import CORS
from src.dynamodb_entrenamiento import DynamoDbEntrenamiento

application = Flask(__name__)
application.register_blueprint(entrenamientos_blueprint)
CORS(application)
dynamo_db_entrenamiento = DynamoDbEntrenamiento()
dynamo_db_entrenamiento.create_table()
## add comment
@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
##
if __name__ == "__main__":
    application.run(host="0.0.0.0", port = 5000, debug = True)