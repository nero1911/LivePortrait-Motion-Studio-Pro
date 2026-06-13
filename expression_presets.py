import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class ExpressionPresets:
    """Manage expression presets for quick animation setup"""
    
    def __init__(self):
        self.presets = {
            "Neutral": {
                "blink_intensity": 50,
                "blink_frequency": 1.0,
                "smile_strength": 0,
                "expression_intensity": 50,
                "head_yaw": 0,
                "head_pitch": 0,
                "head_roll": 0,
                "head_nod_intensity": 10,
                "hair_flutter": 10,
                "hair_direction": 0,
                "breathing_intensity": 20,
                "breathing_frequency": 0.5,
                "eye_gaze_x": 0,
                "eye_gaze_y": 0,
            },
            "Happy": {
                "blink_intensity": 60,
                "blink_frequency": 1.2,
                "smile_strength": 80,
                "expression_intensity": 70,
                "head_yaw": 5,
                "head_pitch": -5,
                "head_roll": 0,
                "head_nod_intensity": 20,
                "hair_flutter": 25,
                "hair_direction": 45,
                "breathing_intensity": 40,
                "breathing_frequency": 0.6,
                "eye_gaze_x": 0,
                "eye_gaze_y": -5,
            },
            "Sad": {
                "blink_intensity": 40,
                "blink_frequency": 0.8,
                "smile_strength": 0,
                "expression_intensity": 40,
                "head_yaw": -10,
                "head_pitch": 10,
                "head_roll": -5,
                "head_nod_intensity": 5,
                "hair_flutter": 5,
                "hair_direction": 180,
                "breathing_intensity": 15,
                "breathing_frequency": 0.4,
                "eye_gaze_x": -10,
                "eye_gaze_y": 10,
            },
            "Confused": {
                "blink_intensity": 55,
                "blink_frequency": 0.9,
                "smile_strength": 20,
                "expression_intensity": 60,
                "head_yaw": 0,
                "head_pitch": -15,
                "head_roll": 5,
                "head_nod_intensity": 15,
                "hair_flutter": 15,
                "hair_direction": 90,
                "breathing_intensity": 25,
                "breathing_frequency": 0.5,
                "eye_gaze_x": 5,
                "eye_gaze_y": 0,
            },
            "Serious": {
                "blink_intensity": 35,
                "blink_frequency": 0.7,
                "smile_strength": 0,
                "expression_intensity": 70,
                "head_yaw": -5,
                "head_pitch": 0,
                "head_roll": 0,
                "head_nod_intensity": 5,
                "hair_flutter": 5,
                "hair_direction": 0,
                "breathing_intensity": 15,
                "breathing_frequency": 0.4,
                "eye_gaze_x": 10,
                "eye_gaze_y": 0,
            },
            "Surprised": {
                "blink_intensity": 70,
                "blink_frequency": 1.5,
                "smile_strength": 50,
                "expression_intensity": 80,
                "head_yaw": 10,
                "head_pitch": -10,
                "head_roll": 0,
                "head_nod_intensity": 25,
                "hair_flutter": 40,
                "hair_direction": 270,
                "breathing_intensity": 50,
                "breathing_frequency": 0.8,
                "eye_gaze_x": 0,
                "eye_gaze_y": -10,
            },
            "Excited": {
                "blink_intensity": 75,
                "blink_frequency": 1.5,
                "smile_strength": 90,
                "expression_intensity": 85,
                "head_yaw": 15,
                "head_pitch": -5,
                "head_roll": 5,
                "head_nod_intensity": 40,
                "hair_flutter": 50,
                "hair_direction": 135,
                "breathing_intensity": 60,
                "breathing_frequency": 1.0,
                "eye_gaze_x": -5,
                "eye_gaze_y": -5,
            },
            "Sleepy": {
                "blink_intensity": 90,
                "blink_frequency": 0.5,
                "smile_strength": 10,
                "expression_intensity": 20,
                "head_yaw": 0,
                "head_pitch": 15,
                "head_roll": 0,
                "head_nod_intensity": 2,
                "hair_flutter": 2,
                "hair_direction": 0,
                "breathing_intensity": 30,
                "breathing_frequency": 0.3,
                "eye_gaze_x": -5,
                "eye_gaze_y": 10,
            },
            "Angry": {
                "blink_intensity": 30,
                "blink_frequency": 0.6,
                "smile_strength": 0,
                "expression_intensity": 100,
                "head_yaw": -15,
                "head_pitch": 5,
                "head_roll": -10,
                "head_nod_intensity": 10,
                "hair_flutter": 20,
                "hair_direction": 180,
                "breathing_intensity": 20,
                "breathing_frequency": 0.3,
                "eye_gaze_x": 15,
                "eye_gaze_y": 5,
            },
            "Contemplative": {
                "blink_intensity": 45,
                "blink_frequency": 0.8,
                "smile_strength": 10,
                "expression_intensity": 55,
                "head_yaw": 20,
                "head_pitch": -5,
                "head_roll": 0,
                "head_nod_intensity": 8,
                "hair_flutter": 8,
                "hair_direction": 45,
                "breathing_intensity": 25,
                "breathing_frequency": 0.4,
                "eye_gaze_x": -20,
                "eye_gaze_y": 0,
            },
            "Idle Loop": {
                "blink_intensity": 50,
                "blink_frequency": 1.0,
                "smile_strength": 15,
                "expression_intensity": 45,
                "head_yaw": 0,
                "head_pitch": 0,
                "head_roll": 0,
                "head_nod_intensity": 15,
                "hair_flutter": 15,
                "hair_direction": 0,
                "breathing_intensity": 30,
                "breathing_frequency": 0.5,
                "eye_gaze_x": 0,
                "eye_gaze_y": 0,
            },
        }
        
        logger.info(f"Loaded {len(self.presets)} expression presets")
    
    def get_preset(self, preset_name: str) -> Optional[Dict]:
        """Get preset by name"""
        if preset_name not in self.presets:
            logger.warning(f"Preset not found: {preset_name}")
            return None
        
        logger.info(f"Applied preset: {preset_name}")
        return self.presets[preset_name].copy()
    
    def get_preset_names(self) -> List[str]:
        """Get all available preset names"""
        return list(self.presets.keys())
    
    def add_custom_preset(self, name: str, params: Dict) -> bool:
        """Add custom preset"""
        if name in self.presets:
            logger.warning(f"Preset already exists: {name}")
            return False
        
        self.presets[name] = params
        logger.info(f"Custom preset added: {name}")
        return True
    
    def remove_preset(self, name: str) -> bool:
        """Remove preset"""
        if name not in self.presets:
            logger.warning(f"Preset not found: {name}")
            return False
        
        del self.presets[name]
        logger.info(f"Preset removed: {name}")
        return True
