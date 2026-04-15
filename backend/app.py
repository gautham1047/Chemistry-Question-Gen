from flask import Flask, request, jsonify
from flask_cors import CORS
import random

import src.problems  # triggers registration
from src.problem_registry import get_modes, get_table_of_contents, invoke_problem, get_all_problems
from src.problems._helpers import polyatomic_ion_test
from chemData import polyatomicIons

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})


def get_polyatomic_choice_list(n):
    nums = [
        [0, 4, 5, 11, 12, 13, 28, 31, 35, 42, 43, 44, 45],
        [0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45],
        [i for i in range(0, 46)]
    ]
    return [list(polyatomicIons.keys())[i] for i in nums[n]]


@app.route('/api/modes', methods=['GET'])
def api_get_modes():
    try:
        return jsonify({"modes": get_modes()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/table-of-contents', methods=['GET'])
def api_get_table_of_contents():
    try:
        return jsonify({"categories": get_table_of_contents()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/question/<int:question_id>', methods=['GET'])
def api_get_question(question_id):
    try:
        rx_type = request.args.get('rxType', '')
        question, answer = invoke_problem(question_id, rx_type)
        return jsonify({
            "question": question,
            "answer": str(answer),
            "questionId": question_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/polyatomic', methods=['GET'])
def api_get_polyatomic():
    try:
        choices_param = request.args.get('choices', '')
        if choices_param:
            choices = choices_param.split(',')
        else:
            choices = list(polyatomicIons.keys())
        question, answer = polyatomic_ion_test(choices)
        return jsonify({"question": question, "answer": str(answer)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/polyatomic-choices/<int:level>', methods=['GET'])
def api_get_polyatomic_choices(level):
    try:
        if level not in [0, 1, 2]:
            return jsonify({"error": "Invalid level. Must be 0, 1, or 2"}), 400
        return jsonify({"choices": get_polyatomic_choice_list(level)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/questions/batch', methods=['POST'])
def api_get_batch_questions():
    try:
        data = request.get_json()
        count = data.get('count', 10)
        question_ids = data.get('questionIds', None)
        rx_types = data.get('rxTypes', [])

        valid_ids = sorted(get_all_problems().keys())
        questions = []

        for i in range(count):
            if question_ids:
                q_id = random.choice([qid for qid in question_ids if qid in valid_ids])
            else:
                q_id = random.choice(valid_ids)

            rx_type = random.choice(rx_types) if rx_types else ''

            try:
                question, answer = invoke_problem(q_id, rx_type)
                questions.append({
                    "id": i + 1,
                    "questionId": q_id,
                    "question": question,
                    "answer": str(answer)
                })
            except Exception as e:
                print(f"Error generating question {q_id}: {str(e)}")
                continue

        return jsonify({"questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/settings', methods=['POST'])
def api_save_settings():
    try:
        data = request.get_json()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
