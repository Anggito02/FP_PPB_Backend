import os
import base64
import traceback
from datetime import datetime

from flask import Blueprint, jsonify, request, send_file

from controller.plate_detection import detect_plate_number

bp = Blueprint("api_bp", __name__)
STORAGE_PATH = os.path.join(os.getcwd(), "resources", "public")

@bp.route("/api/upload-photo", methods=["POST"])
def upload_photo():
    try:
        image = request.json["image"]
        timeNow = datetime.now().strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(STORAGE_PATH, f"{timeNow}.png")

        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image))

        detected_image_path = detect_plate_number(image_path)

        return send_file(detected_image_path)
    except:
        traceback.print_exc()
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500