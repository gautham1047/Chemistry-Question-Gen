from flask import Flask, request, jsonify
from flask_cors import CORS
from inflect import engine
import random
import sys
import io

from chemProblems import *
from chemData import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

inflector = engine()

# Helper function from chemProblems.py
def flaskify(s: str, rxType=""):
    old_std_out = sys.stdout
    capture_io = io.StringIO()
    sys.stdout = capture_io

    try:
        ans = eval(s + f"(rxType = '{rxType}')")
        printed = capture_io.getvalue()
    except Exception as e:
        sys.stdout = old_std_out
        capture_io.close()
        raise e

    sys.stdout = old_std_out
    capture_io.close()

    return [printed, ans]

def polyatomicFlaskied(polyatomicIonChoices):
    old_std_out = sys.stdout
    capture_io = io.StringIO()
    sys.stdout = capture_io

    ans = polyatomicIonTest(polyatomicIonChoices)
    printed = capture_io.getvalue()
    sys.stdout = old_std_out
    capture_io.close()

    return [printed, ans]

# Get all question modes
def get_modes():
    return [
        "SI Units", "Average atomic mass", "Missing Isotope Percentage",
        "Formula to Name", "Name to Formula", "Molar Conversions",
        "Calculate Percent Composition", "Percent Composition to equation (WIP)", "Mass of One Element in a Compound",
        "Complex Percent Composition to Equation",  "Solubility Rules", "Writing Chemical Equations",
        "Basic Stoichiometry", "Percent Yield/Limiting Reagent", "Heat of Physical Change",
        "Coffee Cup Calorimetry", "Bomb Calorimetry", "Average Kinetic Energy",
        "Effusion Rates", "Gas Laws", "Gas Stoiciometry",
        "Electron configuration", "Nobel Gas Shorthand", "Paramagnetic vs Diamagnetic",
        "Quantum Numbers", "Basic Waves",  "Bohr's Law",
        "De Broglie for electrons", "De Broglie in general", "Heisenburg uncertainty principle",
        "Identifying types of waves", "Harder Bohr's Law", "Atomic Size",
        "Ion Size", "Ionization Energy", "Electronegativity",
        "Electron Affinity", "All Periodic Trends", "Lattice Energy",
        "Lewis Dot Structure", "VSEPR", "Bond Order",
        "Sigma and Pi Bonds", "Bond Energies", "Enthalpy from Bond Energies",
        "Solubility Calculations", "Determining Saturation", "Dilution",
        "Solutions Unit Conversions (Aqueous)", "Solutions Unit Conversions (general)", "Colligative Properties",
        "Molar Mass From bp/fp", "Henry's Law", "Reactions with Solubility Units",
        "Hydrates", "Polar vs Nonpolar", "More Thermodynamics", "Basic Concentration",
        "Method of Initial Rates", "Determining the Equilibrium Constant", "Missing Equilibrium Concentration",
        "Calculating K_eq", "Calculating Equilibrium Concentrations from Initial", "pH Conversions",
        "pH from Molarity", "pH with Common Ion Effect", "Neutralization/Tritation Reactions",
        "Solubility Products", "Oxidation Numbers", "Balancing Redox (WIP)",
        "Reaction Potential (WIP)", "Electroplating", "Nuclear Chem"
    ]

# Get table of contents (category groupings)
def get_table_of_contents():
    modes = get_modes()
    def table_of_contents(n):
        return {
            0: [i for i, _ in enumerate(modes)],
            1: [1],
            2: [2, 3, 4, 5],
            3: [6, 7, 8, 9, 10],
            4: [11, 12],
            5: [13, 14],
            6: [15, 16, 17],
            7: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            8: [18, 19, 20, 21],
            9: [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
            10: [i for i in range(33, 46)],
            11: [i for i in range(46, 57)],
            12: [57, 58],
            13: [59, 60, 61, 62],
            14: [63],
            15: [64, 65, 66, 67, 68],
            16: [69, 70, 71, 72],
            17: [73]
        }.get(n)

    categories = [
        {"id": 0, "name": "All", "questionIds": table_of_contents(0)},
        {"id": 1, "name": "Math Review", "questionIds": table_of_contents(1)},
        {"id": 2, "name": "Chemical Nomenclature", "questionIds": table_of_contents(2)},
        {"id": 3, "name": "Chemical Quantities", "questionIds": table_of_contents(3)},
        {"id": 4, "name": "Chemical Reactions", "questionIds": table_of_contents(4)},
        {"id": 5, "name": "Stoichiometry", "questionIds": table_of_contents(5)},
        {"id": 6, "name": "Thermochemistry", "questionIds": table_of_contents(6)},
        {"id": 7, "name": "Semester One", "questionIds": table_of_contents(7)},
        {"id": 8, "name": "Gas Laws", "questionIds": table_of_contents(8)},
        {"id": 9, "name": "Electron Configuration", "questionIds": table_of_contents(9)},
        {"id": 10, "name": "Periodic Trends and Bonds", "questionIds": table_of_contents(10)},
        {"id": 11, "name": "Solutions", "questionIds": table_of_contents(11)},
        {"id": 12, "name": "Rates", "questionIds": table_of_contents(12)},
        {"id": 13, "name": "Equilibrium", "questionIds": table_of_contents(13)},
        {"id": 14, "name": "Thermodynamics", "questionIds": table_of_contents(14)},
        {"id": 15, "name": "Acid-Base", "questionIds": table_of_contents(15)},
        {"id": 16, "name": "Electrochemistry", "questionIds": table_of_contents(16)},
        {"id": 17, "name": "Nuclear Chemistry", "questionIds": table_of_contents(17)}
    ]

    return categories

# Get polyatomic choices by level
def get_polyatomic_choice_list(n):
    nums = [
        [0, 4, 5, 11, 12, 13, 28, 31, 35, 42, 43, 44, 45],
        [0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45],
        [i for i in range(0, 46)]
    ]
    return [list(polyatomicIons.keys())[i] for i in nums[n]]

# ================== API ROUTES ==================

@app.route('/api/modes', methods=['GET'])
def api_get_modes():
    """Get list of all question modes"""
    try:
        modes = get_modes()
        return jsonify({"modes": modes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/table-of-contents', methods=['GET'])
def api_get_table_of_contents():
    """Get category groupings"""
    try:
        categories = get_table_of_contents()
        return jsonify({"categories": categories}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/question/<int:question_id>', methods=['GET'])
def api_get_question(question_id):
    """Get single question by ID"""
    try:
        rx_type = request.args.get('rxType', '')

        # Convert question ID to function name
        func_name = inflector.number_to_words(question_id).replace("-", "")

        # Generate question
        result = flaskify(func_name, rx_type)
        question_text = result[0]
        answer = result[1]

        return jsonify({
            "question": question_text,
            "answer": str(answer),
            "questionId": question_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/polyatomic', methods=['GET'])
def api_get_polyatomic():
    """Get polyatomic ion question"""
    try:
        # Get choices from query params (comma-separated)
        choices_param = request.args.get('choices', '')
        if choices_param:
            choices = choices_param.split(',')
        else:
            # Default to all polyatomic ions
            choices = list(polyatomicIons.keys())

        # Generate question
        result = polyatomicFlaskied(choices)
        question_text = result[0]
        answer = result[1]

        return jsonify({
            "question": question_text,
            "answer": str(answer)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/polyatomic-choices/<int:level>', methods=['GET'])
def api_get_polyatomic_choices(level):
    """Get polyatomic ions for difficulty level (0=difficult, 1=-ates/-ites, 2=all)"""
    try:
        if level not in [0, 1, 2]:
            return jsonify({"error": "Invalid level. Must be 0, 1, or 2"}), 400

        choices = get_polyatomic_choice_list(level)
        return jsonify({"choices": choices}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/questions/batch', methods=['POST'])
def api_get_batch_questions():
    """Get multiple questions at once"""
    try:
        data = request.get_json()
        count = data.get('count', 10)
        question_ids = data.get('questionIds', None)
        rx_types = data.get('rxTypes', [])

        questions = []

        # Valid question IDs (tested and verified to work)
        valid_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 72, 73]

        for i in range(count):
            # Determine question ID
            if question_ids and len(question_ids) > 0:
                q_id = random.choice([qid for qid in question_ids if qid in valid_ids])
            else:
                q_id = random.choice(valid_ids)

            # Determine reaction type (if applicable)
            rx_type = random.choice(rx_types) if rx_types and len(rx_types) > 0 else ''

            try:
                # Generate question
                func_name = inflector.number_to_words(q_id).replace("-", "")
                result = flaskify(func_name, rx_type)

                questions.append({
                    "id": i + 1,
                    "questionId": q_id,
                    "question": result[0],
                    "answer": str(result[1])
                })
            except Exception as e:
                # Skip this question if it fails
                print(f"Error generating question {q_id}: {str(e)}")
                continue

        return jsonify({"questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings', methods=['POST'])
def api_save_settings():
    """Save user settings (optional - for session management if needed)"""
    try:
        data = request.get_json()
        # In a stateless API, we don't actually need to save settings
        # The frontend will manage its own state
        # This endpoint exists for future extensibility
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
