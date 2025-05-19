from flask import Flask, render_template, request, jsonify
import logging
import os
from deconfliction_system import check_conflicts
from test_cases import get_test_case
from visualization import visualize_2d, visualize_3d, visualize_4d_timeline
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "uav-deconfliction-secret")

@app.route('/')
def index():
    """Main route to render the web interface"""
    return render_template('index.html')

@app.route('/api/check_conflicts', methods=['POST'])
def api_check_conflicts():
    """API endpoint to check for conflicts between drone missions"""
    try:
        data = request.json
        primary_mission = data.get('primary_mission')
        other_missions = data.get('other_missions')
        
        # Validate input
        if not primary_mission or not other_missions:
            return jsonify({'error': 'Missing required mission data'}), 400
            
        # Check for conflicts
        status, conflicts = check_conflicts(primary_mission, other_missions)
        
        return jsonify({
            'status': status,
            'conflicts': conflicts
        })
    except Exception as e:
        logger.exception("Error processing conflict check")
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualize/2d', methods=['POST'])
def visualize_2d_api():
    """API endpoint to generate 2D visualization"""
    try:
        data = request.json
        if not data:
            logger.error("No JSON data received in request")
            return jsonify({'error': 'No data received'}), 400
            
        primary_mission = data.get('primary_mission')
        other_missions = data.get('other_missions', [])
        conflicts = data.get('conflicts', [])
        
        if not primary_mission:
            logger.error("Missing primary mission data")
            return jsonify({'error': 'Primary mission data is required'}), 400
        
        # Log debug information
        logger.debug(f"Generating 2D visualization for: {primary_mission}")
        logger.debug(f"With other missions: {len(other_missions)}")
        logger.debug(f"And conflicts: {len(conflicts) if conflicts else 0}")
        
        # Generate visualization
        image_data = visualize_2d(primary_mission, other_missions, conflicts)
        
        if image_data:
            logger.debug("Visualization generated successfully")
            return jsonify({'image': image_data})
        
        logger.error("Visualization failed to generate")
        return jsonify({'error': 'Could not generate visualization'}), 500
    except Exception as e:
        logger.exception("Error generating 2D visualization")
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualize/3d', methods=['POST'])
def visualize_3d_api():
    """API endpoint to generate 3D visualization"""
    try:
        data = request.json
        primary_mission = data.get('primary_mission')
        other_missions = data.get('other_missions', [])
        conflicts = data.get('conflicts', [])
        
        # Generate visualization
        image_data = visualize_3d(primary_mission, other_missions, conflicts)
        
        if image_data:
            return jsonify({'image': image_data})
        return jsonify({'error': 'Could not generate visualization'}), 500
    except Exception as e:
        logger.exception("Error generating 3D visualization")
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualize/4d', methods=['POST'])
def visualize_4d_api():
    """API endpoint to generate 4D timeline visualization"""
    try:
        data = request.json
        primary_mission = data.get('primary_mission')
        other_missions = data.get('other_missions', [])
        conflicts = data.get('conflicts', [])
        
        # Generate visualization
        image_data = visualize_4d_timeline(primary_mission, other_missions, conflicts)
        
        if image_data:
            return jsonify({'image': image_data})
        return jsonify({'error': 'Could not generate timeline visualization'}), 500
    except Exception as e:
        logger.exception("Error generating 4D timeline visualization")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test_cases/<case_id>', methods=['GET'])
def get_test_case_data(case_id):
    """API endpoint to retrieve predefined test cases"""
    try:
        test_case = get_test_case(case_id)
        if test_case:
            return jsonify(test_case)
        return jsonify({'error': 'Test case not found'}), 404
    except Exception as e:
        logger.exception("Error retrieving test case")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
