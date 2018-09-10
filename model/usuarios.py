import base64

from flask import request, jsonify

from app import app
from database import DAO
from model.orgaos_sql import foto_mat_query


@app.route("/api/orgaos/foto", methods=['GET'])
def get_foto():
    cdmat = request.args.get('cdmat')
    data = DAO.run(foto_mat_query, {"mat": cdmat}).fetchone()
    bs4_img = base64.b64encode(data[0].read()).decode()
    return jsonify({"foto": bs4_img})
