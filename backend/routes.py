from flask import Blueprint, jsonify, request, render_template
import os
import pandas as pd
from logic.preprocessing import clean_csv
from logic.apriori_runner import get_rules, get_frequent_itemsets, get_items_list
from logic.visualize import create_heatmap, plot_frequent_items, draw_rules_network, scatter_lift_support


back_bp = Blueprint('back', __name__)

front_bp = Blueprint('front', __name__, static_folder='../frontend/static', template_folder='../frontend/templates')

@front_bp.route('/')
def home():
    return render_template('home.html')

@front_bp.route('/upload')
def upload_page():
    return render_template('upload.html')

@front_bp.route('/analysis')
def analysis_page():
    return render_template('analysis.html')

@front_bp.route('/preprocess')
def preprocess_page():
    return render_template('preprocess.html')

@front_bp.route('/visuals')
def visualize_page():
    return render_template('visuals.html')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

current_file = {"path": None, "name": None}

# ----- Route to upload CSV file -----
@back_bp.route('/upload', methods=['POST'])
def upload_file() -> tuple:
    file =request.files.get('csvFile')

    if not file or not file.filename.endswith('.csv'):
        return jsonify({"error": "Please upload a valid CSV file."}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    df = pd.read_csv(file_path)

    current_file["path"] = file_path
    current_file["name"] = file.filename

    return jsonify({"message": f"File '{file.filename}' uploaded successfully.", "transaction_count": len(df)}), 200

# ----- Route to get CSV file info -----
@back_bp.route('/file_info', methods=['GET'])
def file_info() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 400

    df = pd.read_csv(current_file["path"])
    return jsonify({
        "file_name": current_file["name"],
        "transaction_count": len(df)
    }), 200
    
# ----- Route to pre-process the uploaded CSV file -----
@back_bp.route('/preprocess/stats', methods=['GET', 'POST'])
def preprocess_stats() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    _, stats = clean_csv(current_file["path"])
    return jsonify(stats), 200

@back_bp.route('/preprocess/preview', methods=['GET'])
def preprocess_preview() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    clean_df, _ = clean_csv(current_file["path"])
    preview = clean_df.head(10).to_dict(orient='records')
    return jsonify(preview), 200

# ----- Route to get association rules -----
@back_bp.route('/analysis/rules', methods=['GET', 'POST'])
def analysis_rules() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    min_support = float(request.args.get('minSupport', 0.005))
    min_confidence = float(request.args.get('minConfidence', 0.2))
    min_lift = float(request.args.get('minLift', 1.1))

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

    #Sort rules by confidence in descending order
    rules = sorted(rules, key=lambda x: x['confidence'], reverse=True)

    # Convert antecedents and consequents from frozenset to string for CSV saving
    for rule in rules:
        rule['antecedents'] = '-'.join(rule['antecedents'])
        rule['consequents'] = '-'.join(rule['consequents'])

    # Save rules to a CSV file
    rules_file_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(current_file['name'])[0]}_rules.csv")
    new_rules_df = pd.DataFrame(rules)
    new_rules_df.to_csv(rules_file_path, index=False)

    return jsonify(rules), 200

@back_bp.route('/analysis/summary', methods=['GET'])
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

@back_bp.route('/visualize/heatmap', methods=['GET'])
def visualize_heatmap() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    transactions = get_items_list(current_file["path"])

    encoded_image = create_heatmap(transactions)
    return jsonify({"image": encoded_image}), 200

@back_bp.route('/visualize/frequent_items', methods=['GET'])
def visualize_frequent_items() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    n = int(request.args.get('n', 10))
    freq_items = get_frequent_itemsets(current_file["path"])
    encoded_image = plot_frequent_items(freq_items, n)
    return jsonify({"image": encoded_image}), 200

@back_bp.route('/visualize/rules_network', methods=['GET'])
def visualize_rules_network() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    rules_file_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(current_file['name'])[0]}_rules.csv")
    if not os.path.exists(rules_file_path):
        return jsonify({"error": "No rules file found. Run analysis first."}), 404

    #rules_to_draw = pd.read_csv(rules_file_path)
    #antecendents and consqeuents should be converted to lists
    #if they have multiple items, they are stored as strings separated by '-'
    rules_to_draw = pd.read_csv(rules_file_path)
    rules_to_draw['antecedents'] = rules_to_draw['antecedents'].str.split('-')
    rules_to_draw['consequents'] = rules_to_draw['consequents'].str.split('-')
    #print(rules_to_draw)
    encoded_image = draw_rules_network(rules_to_draw)
    return jsonify({"image": encoded_image}), 200

@back_bp.route('/visualize/scatter_lift_support', methods=['GET'])
def visualize_scatter_lift_support() -> tuple:
    if not current_file["path"]:
        return jsonify({"error": "No file uploaded."}), 404

    rules_file_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(current_file['name'])[0]}_rules.csv")
    if not os.path.exists(rules_file_path):
        return jsonify({"error": "No rules file found. Run analysis first."}), 404
    
    rules = pd.read_csv(rules_file_path)

    encoded_image = scatter_lift_support(rules)
    return jsonify({"image": encoded_image}), 200