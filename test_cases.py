"""
Test cases for UAV deconfliction system.
Provides sample mission data for testing both conflict and conflict-free scenarios.
"""

TEST_CASES = {
    'no_conflict_2d': {
        'primary_mission': {
            'waypoints': [
                [0, 0],
                [10, 10],
                [20, 20],
                [30, 10]
            ],
            'time_window': [0, 100]  # Complete mission between 0 and 100 seconds
        },
        'other_missions': [
            {
                'id': 'drone_1',
                'waypoints': [  # [x, y, timestamp]
                    [50, 50, 10],
                    [60, 40, 30],
                    [70, 50, 50],
                    [80, 60, 70]
                ]
            },
            {
                'id': 'drone_2',
                'waypoints': [
                    [10, 40, 20],
                    [20, 50, 40],
                    [30, 60, 60],
                    [40, 70, 80]
                ]
            }
        ],
        'description': 'No conflict scenario in 2D - all drones have safe distances'
    },
    
    'spatial_conflict_2d': {
        'primary_mission': {
            'waypoints': [
                [0, 0],
                [25, 25],
                [50, 50],
                [75, 25]
            ],
            'time_window': [0, 100]
        },
        'other_missions': [
            {
                'id': 'drone_3',
                'waypoints': [
                    [30, 30, 30],
                    [40, 40, 50],
                    [50, 30, 70],
                    [60, 20, 90]
                ]
            },
            {
                'id': 'drone_4',
                'waypoints': [
                    [10, 40, 20],
                    [20, 50, 40],
                    [40, 60, 70],
                    [60, 70, 90]
                ]
            }
        ],
        'description': 'Spatial conflict scenario in 2D - primary mission conflicts with drone_3'
    },
    
    'temporal_conflict_2d': {
        'primary_mission': {
            'waypoints': [
                [0, 0],
                [20, 20],
                [40, 40],
                [60, 20]
            ],
            'time_window': [0, 100]
        },
        'other_missions': [
            {
                'id': 'drone_5',
                'waypoints': [
                    [10, 10, 10],
                    [30, 30, 40],
                    [50, 50, 70],
                    [70, 70, 100]
                ]
            }
        ],
        'description': 'Temporal conflict scenario in 2D - primary mission and drone_5 conflict in time and space'
    },
    
    'no_conflict_3d': {
        'primary_mission': {
            'waypoints': [
                [0, 0, 10],
                [10, 10, 20],
                [20, 20, 30],
                [30, 10, 40]
            ],
            'time_window': [0, 100]
        },
        'other_missions': [
            {
                'id': 'drone_6',
                'waypoints': [  # [x, y, z, timestamp]
                    [5, 5, 40, 20],
                    [15, 15, 50, 40],
                    [25, 25, 60, 60],
                    [35, 35, 70, 80]
                ]
            },
            {
                'id': 'drone_7',
                'waypoints': [
                    [10, 30, 5, 30],
                    [20, 40, 5, 50],
                    [30, 50, 5, 70],
                    [40, 60, 5, 90]
                ]
            }
        ],
        'description': 'No conflict scenario in 3D - drones at different altitudes'
    },
    
    'altitude_conflict_3d': {
        'primary_mission': {
            'waypoints': [
                [0, 0, 10],
                [10, 10, 20],
                [20, 20, 30],
                [30, 10, 25]
            ],
            'time_window': [0, 100]
        },
        'other_missions': [
            {
                'id': 'drone_8',
                'waypoints': [
                    [15, 15, 20, 40],
                    [25, 25, 25, 60],
                    [35, 35, 30, 80],
                    [45, 45, 35, 100]
                ]
            }
        ],
        'description': 'Altitude conflict scenario in 3D - primary mission and drone_8 conflict in 3D space'
    },
    
    'complex_scenario': {
        'primary_mission': {
            'waypoints': [
                [0, 0, 20],
                [20, 20, 30],
                [40, 40, 40],
                [60, 20, 30],
                [80, 0, 20]
            ],
            'time_window': [0, 200]
        },
        'other_missions': [
            {
                'id': 'drone_9',
                'waypoints': [
                    [10, 10, 10, 20],
                    [30, 30, 20, 60],
                    [50, 50, 30, 100],
                    [70, 70, 40, 140],
                    [90, 90, 50, 180]
                ]
            },
            {
                'id': 'drone_10',
                'waypoints': [
                    [80, 10, 30, 40],
                    [60, 30, 35, 80],
                    [40, 50, 40, 120],
                    [20, 70, 45, 160]
                ]
            },
            {
                'id': 'drone_11',
                'waypoints': [
                    [50, 0, 25, 50],
                    [40, 20, 35, 90],
                    [30, 40, 45, 130],
                    [20, 60, 55, 170]
                ]
            }
        ],
        'description': 'Complex scenario with multiple potential conflicts in 3D space and time'
    }
}

def get_test_case(case_id):
    """
    Get a test case by ID.
    
    Args:
        case_id: ID of the test case to retrieve
        
    Returns:
        Test case data or None if not found
    """
    return TEST_CASES.get(case_id)

def list_test_cases():
    """
    List all available test cases.
    
    Returns:
        List of test case IDs and descriptions
    """
    return [
        {'id': case_id, 'description': data.get('description', 'No description')}
        for case_id, data in TEST_CASES.items()
    ]
