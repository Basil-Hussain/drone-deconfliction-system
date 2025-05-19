import numpy as np
import logging
from typing import List, Dict, Tuple, Union, Any
import math

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Minimum safe distance between drones (in meters)
MIN_SAFE_DISTANCE_2D = 10.0  
MIN_SAFE_DISTANCE_3D = 10.0

def check_conflicts(primary_mission: Dict, other_missions: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    Check for conflicts between a primary drone mission and other drone missions.
    
    Args:
        primary_mission: Dict containing:
            - waypoints: List of waypoints [(x, y, z?)]
            - time_window: [start_time, end_time] in seconds
        other_missions: List of dictionaries, each containing:
            - id: Unique identifier for the mission
            - waypoints: List of waypoints with timestamps [(x, y, z?, timestamp)]
    
    Returns:
        status: "clear" or "conflict detected"
        conflicts: List of conflict details or empty list if no conflicts
    """
    logger.debug(f"Checking conflicts for primary mission: {primary_mission}")
    
    # Extract primary mission details
    primary_waypoints = primary_mission.get('waypoints', [])
    primary_time_window = primary_mission.get('time_window', [0, 0])
    
    # Determine if we're working in 2D or 3D
    is_3d = len(primary_waypoints[0]) > 2 if primary_waypoints else False
    
    # Estimated time to complete each segment of the primary mission
    primary_timeline = estimate_mission_timeline(primary_waypoints, primary_time_window)
    
    conflicts = []
    
    # Check for conflicts with each other mission
    for other_mission in other_missions:
        mission_id = other_mission.get('id', 'unknown')
        other_waypoints_with_time = other_mission.get('waypoints', [])
        
        # Skip if other mission has no waypoints
        if not other_waypoints_with_time:
            continue
            
        # Interpolate other mission path for full trajectory
        other_trajectory = interpolate_trajectory(other_waypoints_with_time)
        
        # Check each segment of the primary mission
        for i in range(len(primary_waypoints) - 1):
            start_point = primary_waypoints[i]
            end_point = primary_waypoints[i+1]
            segment_start_time = primary_timeline[i]
            segment_end_time = primary_timeline[i+1]
            
            # Check spatial and temporal conflicts
            segment_conflicts = check_segment_conflicts(
                start_point, end_point,
                segment_start_time, segment_end_time,
                other_trajectory, mission_id,
                is_3d
            )
            
            conflicts.extend(segment_conflicts)
    
    # Determine status based on presence of conflicts
    status = "conflict detected" if conflicts else "clear"
    
    logger.debug(f"Conflict check complete. Status: {status}, Conflicts: {len(conflicts)}")
    return status, conflicts

def estimate_mission_timeline(waypoints: List, time_window: List[float]) -> List[float]:
    """
    Estimate timestamps for each waypoint based on mission time window.
    
    Args:
        waypoints: List of waypoints
        time_window: [start_time, end_time] in seconds
    
    Returns:
        List of timestamps for each waypoint
    """
    if not waypoints:
        return []
        
    start_time, end_time = time_window
    mission_duration = end_time - start_time
    
    # Calculate total distance to estimate time proportionally
    total_distance = 0
    for i in range(len(waypoints) - 1):
        total_distance += calculate_distance(waypoints[i], waypoints[i+1])
    
    # If no distance (single waypoint or identical points), assume equal time distribution
    if total_distance == 0:
        return [start_time + (mission_duration * i / max(1, len(waypoints) - 1)) for i in range(len(waypoints))]
    
    # Distribute time based on segment distances
    timeline = [start_time]
    cumulative_distance = 0
    
    for i in range(len(waypoints) - 1):
        segment_distance = calculate_distance(waypoints[i], waypoints[i+1])
        cumulative_distance += segment_distance
        segment_time = start_time + (mission_duration * cumulative_distance / total_distance)
        timeline.append(segment_time)
    
    return timeline

def calculate_distance(point1: List[float], point2: List[float]) -> float:
    """
    Calculate Euclidean distance between two points (2D or 3D).
    
    Args:
        point1: First point [x, y] or [x, y, z]
        point2: Second point [x, y] or [x, y, z]
    
    Returns:
        Euclidean distance
    """
    # Ensure points have the same dimensions
    dim = min(len(point1), len(point2))
    
    return math.sqrt(sum((point1[i] - point2[i]) ** 2 for i in range(dim)))

def interpolate_trajectory(waypoints_with_time: List) -> List[Dict]:
    """
    Interpolate a complete trajectory from waypoints with timestamps.
    
    Args:
        waypoints_with_time: List of [x, y, z?, timestamp] points
    
    Returns:
        List of {position: [x, y, z?], time: timestamp} dictionaries
    """
    trajectory = []
    
    # Sort waypoints by timestamp
    sorted_waypoints = sorted(waypoints_with_time, key=lambda x: x[-1])
    
    # Add each waypoint to the trajectory
    for waypoint in sorted_waypoints:
        position = waypoint[:-1]  # All elements except the last (timestamp)
        time = waypoint[-1]
        trajectory.append({
            'position': position,
            'time': time
        })
    
    return trajectory

def check_segment_conflicts(
    start_point: List[float],
    end_point: List[float], 
    start_time: float,
    end_time: float,
    other_trajectory: List[Dict],
    other_mission_id: str,
    is_3d: bool
) -> List[Dict]:
    """
    Check for conflicts between a primary mission segment and another drone's trajectory.
    
    Args:
        start_point: Starting point of segment [x, y] or [x, y, z]
        end_point: Ending point of segment [x, y] or [x, y, z]
        start_time: Start time of segment
        end_time: End time of segment
        other_trajectory: List of trajectory points with timestamps
        other_mission_id: ID of the other mission
        is_3d: Flag indicating if working in 3D
    
    Returns:
        List of conflict dictionaries with details
    """
    conflicts = []
    min_safe_distance = MIN_SAFE_DISTANCE_3D if is_3d else MIN_SAFE_DISTANCE_2D
    
    # Filter other trajectory points within the segment's time window
    relevant_trajectory = [
        point for point in other_trajectory 
        if point['time'] >= start_time and point['time'] <= end_time
    ]
    
    # If no relevant points, no temporal overlap
    if not relevant_trajectory:
        return conflicts
    
    # For each point in the filtered trajectory, check spatial conflict
    for traj_point in relevant_trajectory:
        other_position = traj_point['position']
        other_time = traj_point['time']
        
        # Interpolate primary position at this time
        primary_position = interpolate_position(
            start_point, end_point, 
            start_time, end_time, 
            other_time
        )
        
        # Calculate distance
        distance = calculate_distance(primary_position, other_position)
        
        # Check if distance is less than minimum safe distance
        if distance < min_safe_distance:
            conflict = {
                'location': {
                    'primary': primary_position,
                    'other': other_position
                },
                'time': other_time,
                'distance': distance,
                'mission_id': other_mission_id,
                'severity': calculate_severity(distance, min_safe_distance)
            }
            conflicts.append(conflict)
    
    return conflicts

def interpolate_position(
    start_point: List[float], 
    end_point: List[float], 
    start_time: float, 
    end_time: float, 
    target_time: float
) -> List[float]:
    """
    Interpolate position at a given time between two waypoints.
    
    Args:
        start_point: Starting position
        end_point: Ending position
        start_time: Start time
        end_time: End time
        target_time: Time to interpolate at
    
    Returns:
        Interpolated position
    """
    # Clamp target_time to the segment time limits
    target_time = max(start_time, min(end_time, target_time))
    
    # Calculate time ratio (0.0 to 1.0)
    time_range = end_time - start_time
    if time_range == 0:
        ratio = 0  # Avoid division by zero
    else:
        ratio = (target_time - start_time) / time_range
    
    # Linear interpolation for each dimension
    position = [
        start_point[i] + ratio * (end_point[i] - start_point[i])
        for i in range(min(len(start_point), len(end_point)))
    ]
    
    return position

def calculate_severity(distance: float, min_safe_distance: float) -> str:
    """
    Calculate severity level based on how close drones are to minimum safe distance.
    
    Args:
        distance: Actual distance between drones
        min_safe_distance: Minimum safe distance threshold
    
    Returns:
        Severity level as string
    """
    ratio = distance / min_safe_distance
    
    if ratio < 0.5:
        return "critical"
    elif ratio < 0.75:
        return "high"
    elif ratio < 1.0:
        return "medium"
    else:
        return "low"  # This should not happen as we filter for < min_safe_distance
