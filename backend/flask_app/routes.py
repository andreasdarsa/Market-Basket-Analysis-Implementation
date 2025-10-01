from flask import Blueprint, jsonify, request
import os
import pandas as pd
from logic.preprocessing import clean_csv
from logic.apriori_runner import get_rules
from logic.visualize import create_heatmap, plot_frequent_items, draw_rules_network, scatter_lift_support

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

current_file = {"path": None, "name": None}

# ----- Route to upload CSV file -----
@routes.route('/api/upload', methods=['POST'])
def upload_file() -> tuple:
    file =request.files.get('file')

    if not file or not file.filename.endswith('.csv'):
        return jsonify({"error": "Please upload a valid CSV file."}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    df = pd.read_csv(file_path)

    current_file["path"] = file_path
    current_file["name"] = file.filename

    return jsonify({"message": f"File '{file.filename}' uploaded successfully.", "transaction_count": len(df)}), 200

# ----- Route to get CSV file info -----
@routes.route('/api/file_info', methods=['GET'])
def file_info() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 400

    df = pd.read_csv(current_file["path"])
    return jsonify({
        "file_name": current_file["name"],
        "transaction_count": len(df)
    }), 200
    
# ----- Route to pre-process the uploaded CSV file -----
@routes.route('/api/preprocess/stats', methods=['POST'])
def preprocess_stats() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    _, stats = clean_csv(current_file["path"])
    return jsonify(stats), 200

@routes.route('/api/preprocess/preview', methods=['GET'])
def preprocess_preview() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    clean_df, _ = clean_csv(current_file["path"])
    preview = clean_df.head(10).to_dict(orient='records')
    return jsonify(preview), 200

# ----- Route to get association rules -----
@routes.route('/api/analysis/rules', methods=['GET'])
def analysis_rules() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    min_support = float(request.args.get('min_support', 0.005))
    min_confidence = float(request.args.get('min_confidence', 0.2))
    min_lift = float(request.args.get('min_lift', 1.1))

    rules_df = get_rules(current_file["path"], min_support, min_confidence, min_lift)
    rules = []

    for _, row in rules_df.iterrows():
        rules.append({
            "antecedents": list(row['antecedents']),
            "consequents": list(row['consequents']),
            "support": row['support'],
            "confidence": row['confidence'],
            "lift": row['lift']
        })

    return jsonify(rules), 200

@routes.route('/api/analysis/summary', methods=['GET'])
def analysis_summary() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    min_support = float(request.args.get('min_support', 0.005))
    min_confidence = float(request.args.get('min_confidence', 0.2))
    min_lift = float(request.args.get('min_lift', 1.1))

    rules_df = get_rules(current_file["path"], min_support, min_confidence, min_lift)
    total_rules = len(rules_df)

    if total_rules == 0:
        return jsonify({
            "total_rules": 0,
            "message": "No rules found with the given parameters."
        }), 200

    avg_support = rules_df['support'].mean()
    avg_confidence = rules_df['confidence'].mean()
    avg_lift = rules_df['lift'].mean()

    return jsonify({
        "total_rules": total_rules,
        "average_support": avg_support,
        "average_confidence": avg_confidence,
        "average_lift": avg_lift
    }), 200