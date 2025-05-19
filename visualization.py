import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Dict, Tuple, Any
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def visualize_2d(
    primary_mission: Dict,
    other_missions: List[Dict],
    conflicts: List[Dict] = [],
    title: str = "UAV Mission Visualization"
) -> str:
    """
    Generate a 2D visualization of drone missions and conflicts.
    
    Args:
        primary_mission: Primary drone mission data
        other_missions: List of other drone missions
        conflicts: List of detected conflicts
        title: Plot title
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Create figure
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
        
        # Extract data
        primary_waypoints = primary_mission.get('waypoints', [])
        primary_time_window = primary_mission.get('time_window', [0, 0])
        
        # Plot primary mission
        primary_x = [p[0] for p in primary_waypoints]
        primary_y = [p[1] for p in primary_waypoints]
        
        # Plot primary mission path
        plt.plot(primary_x, primary_y, 'b-', linewidth=2, label='Primary Mission')
        plt.scatter(primary_x, primary_y, color='blue', s=50, marker='o')
        
        # Annotate primary waypoints
        for i, (x, y) in enumerate(zip(primary_x, primary_y)):
            plt.annotate(f"P{i+1}", (x, y), textcoords="offset points", 
                         xytext=(0, 10), ha='center')
        
        # Plot other missions
        colors = ['green', 'red', 'purple', 'orange', 'brown', 'pink']
        
        for i, mission in enumerate(other_missions):
            mission_id = mission.get('id', f'Mission {i+1}')
            waypoints = mission.get('waypoints', [])
            
            if not waypoints:
                continue
                
            # Get color for this mission
            color_idx = i % len(colors)
            color = colors[color_idx]
            
            # Extract x, y, timestamps
            other_x = [p[0] for p in waypoints]
            other_y = [p[1] for p in waypoints]
            
            # Plot mission path
            plt.plot(other_x, other_y, '-', color=color, linewidth=1.5, 
                     alpha=0.7, label=f'{mission_id}')
            plt.scatter(other_x, other_y, color=color, s=30, marker='s')
            
            # Annotate waypoints
            for j, (x, y) in enumerate(zip(other_x, other_y)):
                plt.annotate(f"{mission_id}-{j+1}", (x, y), 
                             textcoords="offset points", xytext=(0, 10), 
                             ha='center', fontsize=8)
        
        # Plot conflicts if provided
        if conflicts:
            for i, conflict in enumerate(conflicts):
                # Extract conflict location
                loc = conflict.get('location', {})
                primary_pos = loc.get('primary', [0, 0])
                other_pos = loc.get('other', [0, 0])
                severity = conflict.get('severity', 'medium')
                
                # Choose color based on severity
                conflict_color = {
                    'critical': 'darkred',
                    'high': 'red',
                    'medium': 'orange',
                    'low': 'yellow'
                }.get(severity, 'red')
                
                # Draw circle around conflict area
                from matplotlib.patches import Circle
                conflict_circle = Circle(
                    (primary_pos[0], primary_pos[1]), 
                    10, color=conflict_color, 
                    fill=False, linestyle='--', linewidth=2, alpha=0.7
                )
                ax.add_patch(conflict_circle)
                
                # Connect conflict points with a line
                plt.plot([primary_pos[0], other_pos[0]], 
                         [primary_pos[1], other_pos[1]], 
                         'r-', linewidth=1, alpha=0.5)
                
                # Add conflict marker
                plt.scatter([primary_pos[0]], [primary_pos[1]], 
                           color=conflict_color, s=100, marker='x')
                
                # Add conflict annotation
                plt.annotate(f"Conflict {i+1}", (primary_pos[0], primary_pos[1]), 
                            textcoords="offset points", xytext=(10, 10), 
                            ha='center', color=conflict_color, fontweight='bold')
        
        # Set plot attributes
        plt.title(title)
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper right', fontsize=10)
        
        # Generate image
        img_data = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        
        # Encode image to base64
        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
        plt.close()
        
        return encoded_img
        
    except Exception as e:
        logger.exception("Error generating 2D visualization")
        return ""

def visualize_3d(
    primary_mission: Dict,
    other_missions: List[Dict],
    conflicts: List[Dict] = [],
    title: str = "UAV 3D Mission Visualization"
) -> str:
    """
    Generate a 3D visualization of drone missions and conflicts.
    
    Args:
        primary_mission: Primary drone mission data
        other_missions: List of other drone missions
        conflicts: List of detected conflicts
        title: Plot title
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Create 3D figure
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Extract data
        primary_waypoints = primary_mission.get('waypoints', [])
        
        # Plot primary mission
        primary_x = [p[0] for p in primary_waypoints]
        primary_y = [p[1] for p in primary_waypoints]
        primary_z = [p[2] for p in primary_waypoints] if len(primary_waypoints[0]) > 2 else [0] * len(primary_waypoints)
        
        # Plot primary mission path
        ax.plot(primary_x, primary_y, primary_z, 'b-', linewidth=2, label='Primary Mission')
        ax.scatter(primary_x, primary_y, primary_z, color='blue', marker='o', s=50)
        
        # Plot other missions
        colors = ['green', 'red', 'purple', 'orange', 'brown', 'pink']
        
        for i, mission in enumerate(other_missions):
            mission_id = mission.get('id', f'Mission {i+1}')
            waypoints = mission.get('waypoints', [])
            
            if not waypoints:
                continue
                
            # Get color for this mission
            color_idx = i % len(colors)
            color = colors[color_idx]
            
            # Extract x, y, z, timestamps
            has_z = len(waypoints[0]) > 3
            other_x = [p[0] for p in waypoints]
            other_y = [p[1] for p in waypoints]
            other_z = [p[2] for p in waypoints] if has_z else [0] * len(waypoints)
            
            # Plot mission path
            ax.plot(other_x, other_y, other_z, '-', color=color, linewidth=1.5, 
                   alpha=0.7, label=f'{mission_id}')
            ax.scatter(other_x, other_y, other_z, color=color, marker='s', s=30)
        
        # Plot conflicts if provided
        if conflicts:
            for i, conflict in enumerate(conflicts):
                # Extract conflict location
                loc = conflict.get('location', {})
                primary_pos = loc.get('primary', [0, 0, 0])
                other_pos = loc.get('other', [0, 0, 0])
                
                # Ensure 3D coordinates
                if len(primary_pos) < 3:
                    primary_pos = list(primary_pos) + [0] * (3 - len(primary_pos))
                if len(other_pos) < 3:
                    other_pos = list(other_pos) + [0] * (3 - len(other_pos))
                
                # Connect conflict points with a line
                ax.plot([primary_pos[0], other_pos[0]], 
                       [primary_pos[1], other_pos[1]], 
                       [primary_pos[2], other_pos[2]], 
                       'r-', linewidth=1, alpha=0.5)
                
                # Add conflict marker
                ax.scatter([primary_pos[0]], [primary_pos[1]], [primary_pos[2]], 
                          color='red', marker='x', s=100)
        
        # Set plot attributes
        ax.set_title(title)
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        
        # Check if 3D axes and set Z label
        if hasattr(ax, 'set_zlabel'):
            ax.set_zlabel('Altitude (Z)')
            
        ax.legend(loc='upper right', fontsize=10)
        
        # Generate image
        img_data = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        
        # Encode image to base64
        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
        plt.close()
        
        return encoded_img
        
    except Exception as e:
        logger.exception("Error generating 3D visualization")
        return ""

def visualize_4d_timeline(
    primary_mission: Dict,
    other_missions: List[Dict],
    conflicts: List[Dict] = [],
    title: str = "UAV Mission Timeline (4D)"
) -> str:
    """
    Generate a timeline visualization showing the temporal aspect of missions.
    
    Args:
        primary_mission: Primary drone mission data
        other_missions: List of other drone missions
        conflicts: List of detected conflicts
        title: Plot title
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Create figure
        plt.figure(figsize=(12, 6))
        
        # Extract data
        primary_waypoints = primary_mission.get('waypoints', [])
        primary_time_window = primary_mission.get('time_window', [0, 0])
        start_time, end_time = primary_time_window
        
        # Create a timeline for primary mission
        mission_times = np.linspace(start_time, end_time, len(primary_waypoints))
        
        # Plot primary mission timeline
        plt.plot([start_time, end_time], [1, 1], 'b-', linewidth=4, alpha=0.7)
        plt.scatter(mission_times, [1] * len(mission_times), color='blue', s=50, marker='o')
        
        # Plot other missions
        colors = ['green', 'red', 'purple', 'orange', 'brown', 'pink']
        
        for i, mission in enumerate(other_missions):
            mission_id = mission.get('id', f'Mission {i+1}')
            waypoints = mission.get('waypoints', [])
            
            if not waypoints:
                continue
                
            # Get color for this mission
            color_idx = i % len(colors)
            color = colors[color_idx]
            
            # Extract timestamps (last element of each waypoint)
            other_times = [p[-1] for p in waypoints]
            min_time = min(other_times)
            max_time = max(other_times)
            
            # Plot mission timeline
            plt.plot([min_time, max_time], [i + 2, i + 2], f"{color}-", linewidth=4, alpha=0.7)
            plt.scatter(other_times, [i + 2] * len(other_times), color=color, s=30, marker='s')
            
            # Add mission label
            plt.text(min_time - 0.5, i + 2, mission_id, ha='right', va='center')
        
        # Plot conflicts if provided
        if conflicts:
            for conflict in conflicts:
                conflict_time = conflict.get('time', 0)
                mission_id = conflict.get('mission_id', 'unknown')
                
                # Find mission index
                mission_idx = next((i for i, m in enumerate(other_missions) 
                                    if m.get('id') == mission_id), 0)
                
                # Draw conflict indicator
                plt.vlines(conflict_time, 1, mission_idx + 2, colors='red', 
                           linestyles='dotted', linewidth=1.5)
                plt.scatter([conflict_time], [mission_idx + 2], color='red', 
                           s=100, marker='x')
                plt.scatter([conflict_time], [1], color='red', 
                           s=100, marker='x')
        
        # Set plot attributes
        plt.title(title)
        plt.xlabel('Time (seconds)')
        plt.yticks([1] + list(range(2, len(other_missions) + 2)), 
                  ['Primary'] + [f'Mission {i+1}' for i in range(len(other_missions))])
        plt.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.xlim(start_time - 1, end_time + 1)
        
        # Generate image
        img_data = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        
        # Encode image to base64
        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
        plt.close()
        
        return encoded_img
        
    except Exception as e:
        logger.exception("Error generating 4D timeline visualization")
        return ""
