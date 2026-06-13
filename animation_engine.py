import torch
import numpy as np
from PIL import Image, ImageDraw
import cv2
import logging
from typing import Optional, Dict, List, Tuple
import math
from scipy.ndimage import gaussian_filter

logger = logging.getLogger(__name__)

class FacialLandmarks:
    """Face landmark detection using OpenCV"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
    
    def detect_face(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detect face region"""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Return largest face
        face = max(faces, key=lambda x: x[2] * x[3])
        return tuple(face)
    
    def get_face_landmarks(self, frame: np.ndarray) -> Optional[Dict]:
        """Get approximate facial landmarks"""
        face = self.detect_face(frame)
        if face is None:
            return None
        
        x, y, w, h = face
        landmarks = {
            'face': (x, y, w, h),
            'left_eye': (int(x + w * 0.3), int(y + h * 0.35)),
            'right_eye': (int(x + w * 0.7), int(y + h * 0.35)),
            'nose': (int(x + w * 0.5), int(y + h * 0.45)),
            'mouth': (int(x + w * 0.5), int(y + h * 0.65)),
        }
        
        return landmarks

class AnimationParameters:
    """Animation parameter management"""
    
    def __init__(self):
        self.blink_intensity = 50
        self.blink_frequency = 1.0
        self.smile_strength = 30
        self.expression_intensity = 50
        self.head_yaw = 0
        self.head_pitch = 0
        self.head_roll = 0
        self.head_nod_intensity = 30
        self.hair_flutter = 20
        self.hair_direction = 0
        self.breathing_intensity = 30
        self.breathing_frequency = 0.5
        self.eye_gaze_x = 0
        self.eye_gaze_y = 0
    
    def update(self, **kwargs):
        """Update parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class AnimationEngine:
    """Main animation generation engine"""
    
    def __init__(self, device: str = "cuda"):
        self.device = device
        self.landmarks_detector = FacialLandmarks()
        self.animation_params = AnimationParameters()
        
        logger.info(f"AnimationEngine initialized on {device}")
    
    def generate_animation(
        self,
        image: Image.Image,
        preview_mode: bool = True,
        duration: float = 3.0,
        fps: int = 30,
        **animation_params
    ) -> Optional[List[np.ndarray]]:
        """Generate animation frames"""
        try:
            logger.info(f"Generating animation ({'preview' if preview_mode else 'final'} mode)")
            
            # Update parameters
            self.animation_params.update(**animation_params)
            
            # Convert PIL image to numpy
            base_image = np.array(image)
            if base_image.shape[2] == 4:
                base_image = base_image[:, :, :3]
            
            # Generate frames
            if preview_mode:
                frames = self._generate_preview_frames(base_image, duration, fps)
            else:
                frames = self._generate_final_frames(base_image, duration, fps)
            
            logger.info(f"Generated {len(frames)} frames")
            return frames
        
        except Exception as e:
            logger.error(f"Animation generation error: {str(e)}")
            return None
    
    def _generate_preview_frames(
        self,
        base_image: np.ndarray,
        duration: float,
        fps: int
    ) -> List[np.ndarray]:
        """Generate preview frames (low quality, fast)"""
        
        # Preview settings
        preview_fps = 15
        preview_duration = min(2.0, duration)
        num_frames = int(preview_fps * preview_duration)
        
        frames = []
        
        for frame_idx in range(num_frames):
            t = frame_idx / preview_fps
            progress = t / preview_duration
            
            frame = self._apply_animation(
                base_image,
                t,
                progress
            )
            
            frames.append(frame)
        
        return frames
    
    def _generate_final_frames(
        self,
        base_image: np.ndarray,
        duration: float,
        fps: int
    ) -> List[np.ndarray]:
        """Generate final frames (high quality)"""
        
        num_frames = int(fps * duration)
        frames = []
        
        for frame_idx in range(num_frames):
            t = frame_idx / fps
            progress = t / duration
            
            frame = self._apply_animation(
                base_image,
                t,
                progress
            )
            
            frames.append(frame)
        
        return frames
    
    def _apply_animation(
        self,
        image: np.ndarray,
        time: float,
        progress: float
    ) -> np.ndarray:
        """Apply animation effects to frame"""
        
        frame = image.copy().astype(np.float32)
        h, w = frame.shape[:2]
        
        # Eye blinking
        frame = self._apply_eye_blink(frame, time)
        
        # Head movement
        frame = self._apply_head_movement(frame, time)
        
        # Facial expression
        frame = self._apply_facial_expression(frame, time)
        
        # Hair flutter
        frame = self._apply_hair_flutter(frame, time)
        
        # Breathing
        frame = self._apply_breathing(frame, time)
        
        # Eye gaze
        frame = self._apply_eye_gaze(frame, time)
        
        # Clamp values
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        
        return frame
    
    def _apply_eye_blink(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply eye blinking animation"""
        params = self.animation_params
        
        # Blink cycle
        blink_cycle = (time * params.blink_frequency) % 1.0
        
        # Blink opens eyes from 0.7-1.0, closes from 0.0-0.3
        if blink_cycle < 0.1:
            blink_amount = blink_cycle / 0.1  # Opening
        elif blink_cycle < 0.2:
            blink_amount = (0.2 - blink_cycle) / 0.1  # Closing
        else:
            blink_amount = 1.0  # Eyes open
        
        intensity_factor = params.blink_intensity / 100.0
        blink_effect = (1.0 - blink_amount) * intensity_factor
        
        # Apply darkening to eye area (simplified)
        if blink_effect > 0:
            h, w = frame.shape[:2]
            # Darken upper portion slightly
            for y in range(int(h * 0.25), int(h * 0.45)):
                for x in range(w):
                    frame[y, x] = frame[y, x] * (1.0 - blink_effect * 0.3)
        
        return frame
    
    def _apply_head_movement(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply head rotation and movement"""
        params = self.animation_params
        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        
        # Nod animation (head_nod_intensity)
        nod_factor = params.head_nod_intensity / 100.0
        nod_amount = math.sin(time * 2 * math.pi) * nod_factor * 2  # -2 to +2 pixels
        
        # Static head angles
        yaw_angle = params.head_yaw * 0.5  # Reduce effect for stability
        pitch_angle = params.head_pitch * 0.5
        roll_angle = params.head_roll * 0.5
        
        # Create transformation matrix
        angle = roll_angle + nod_amount
        scale = 1.0
        
        M = cv2.getRotationMatrix2D(center, angle, scale)
        
        # Apply transformation
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        
        return frame
    
    def _apply_facial_expression(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply facial expressions (smile, etc.)"""
        params = self.animation_params
        
        # Smile animation (subtle)
        smile_factor = params.smile_strength / 100.0
        
        # Expression intensity
        expr_factor = params.expression_intensity / 100.0
        
        # Apply expression by slightly modifying pixel colors
        if smile_factor > 0 or expr_factor > 0:
            h, w = frame.shape[:2]
            
            # Brighten cheek areas for smile effect
            for y in range(int(h * 0.4), int(h * 0.65)):
                for x in range(w):
                    if x < w // 2:
                        # Left cheek
                        frame[y, x] = frame[y, x] * (1.0 + smile_factor * 0.1)
                    else:
                        # Right cheek
                        frame[y, x] = frame[y, x] * (1.0 + smile_factor * 0.1)
            
            # Add subtle color variation for expression
            frame[:, :, 0] = frame[:, :, 0] * (1.0 - expr_factor * 0.05)  # R
            frame[:, :, 1] = frame[:, :, 1] * (1.0 + expr_factor * 0.05)  # G
        
        return frame
    
    def _apply_hair_flutter(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply hair flutter effect"""
        params = self.animation_params
        
        if params.hair_flutter < 5:
            return frame
        
        h, w = frame.shape[:2]
        flutter_factor = params.hair_flutter / 100.0
        
        # Create flutter displacement
        angle_rad = math.radians(params.hair_direction)
        flutter_amount = math.sin(time * 3) * flutter_factor * 3  # -3 to +3 pixels
        
        dx = int(flutter_amount * math.cos(angle_rad))
        dy = int(flutter_amount * math.sin(angle_rad))
        
        # Apply displacement to top portion (hair area)
        if abs(dx) > 0 or abs(dy) > 0:
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        
        return frame
    
    def _apply_breathing(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply breathing animation"""
        params = self.animation_params
        
        if params.breathing_intensity < 5:
            return frame
        
        h, w = frame.shape[:2]
        breathing_factor = params.breathing_intensity / 100.0
        
        # Breathing cycle
        breath_scale = 1.0 + math.sin(time * params.breathing_frequency * 2 * math.pi) * 0.02 * breathing_factor
        
        # Apply subtle scaling to chest area
        center = (w // 2, h)
        M = cv2.getRotationMatrix2D(center, 0, breath_scale)
        
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        
        return frame
    
    def _apply_eye_gaze(self, frame: np.ndarray, time: float) -> np.ndarray:
        """Apply eye gaze direction"""
        params = self.animation_params
        
        if params.eye_gaze_x == 0 and params.eye_gaze_y == 0:
            return frame
        
        h, w = frame.shape[:2]
        
        # Gaze displacement
        gaze_dx = int(params.eye_gaze_x * 0.1)
        gaze_dy = int(params.eye_gaze_y * 0.1)
        
        if abs(gaze_dx) > 0 or abs(gaze_dy) > 0:
            M = np.float32([[1, 0, gaze_dx], [0, 1, gaze_dy]])
            frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        
        return frame
