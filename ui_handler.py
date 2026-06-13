import os
import cv2
import numpy as np
from pathlib import Path
import logging
from typing import List, Optional
import tempfile
import imageio

logger = logging.getLogger(__name__)

class UIHandler:
    """Handle UI-related tasks like video saving and previews"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.output_dir = Path.home() / "LivePortrait_Output"
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"Output directory: {self.output_dir}")
    
    def create_preview_video(self, frames: List[np.ndarray], fps: int = 15) -> Optional[str]:
        """Create preview video file"""
        try:
            if not frames:
                logger.error("No frames provided")
                return None
            
            preview_path = os.path.join(self.temp_dir, "preview.mp4")
            
            # Use imageio to save
            imageio.mimwrite(preview_path, frames, fps=fps, codec='libx264')
            
            logger.info(f"Preview created: {preview_path}")
            return preview_path
        
        except Exception as e:
            logger.error(f"Preview creation error: {str(e)}")
            return None
    
    def save_video(
        self,
        frames: List[np.ndarray],
        output_format: str = "MP4",
        fps: int = 30,
        output_size: tuple = (854, 480)
    ) -> Optional[str]:
        """Save video with user settings"""
        try:
            if not frames:
                logger.error("No frames to save")
                return None
            
            # Resize frames if needed
            resized_frames = []
            for frame in frames:
                resized = cv2.resize(frame, output_size, interpolation=cv2.INTER_LANCZOS4)
                resized_frames.append(resized)
            
            # Generate filename
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format == "MP4":
                filename = f"animation_{timestamp}.mp4"
                output_path = self.output_dir / filename
                
                # Save MP4
                imageio.mimwrite(
                    str(output_path),
                    resized_frames,
                    fps=fps,
                    codec='libx264',
                    pixelformat='yuv420p'
                )
            
            elif output_format == "GIF":
                filename = f"animation_{timestamp}.gif"
                output_path = self.output_dir / filename
                
                # Reduce fps for GIF
                gif_fps = min(fps, 15)
                duration = 1000 / gif_fps  # Duration per frame in ms
                
                # Convert frames for GIF
                gif_frames = []
                for frame in resized_frames:
                    # Convert BGR to RGB if needed
                    if frame.shape[2] == 3:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    gif_frames.append(frame)
                
                imageio.mimwrite(
                    str(output_path),
                    gif_frames,
                    duration=duration,
                    loop=0
                )
            
            else:
                logger.error(f"Unsupported format: {output_format}")
                return None
            
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            logger.info(f"Saved {output_format}: {output_path} ({file_size:.2f}MB)")
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Video save error: {str(e)}")
            return None
    
    def get_output_directory(self) -> str:
        """Get output directory path"""
        return str(self.output_dir)
    
    def open_output_directory(self):
        """Open output directory in file explorer"""
        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(self.output_dir)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.output_dir])
            else:
                subprocess.Popen(["xdg-open", self.output_dir])
            
            logger.info("Opening output directory")
        
        except Exception as e:
            logger.error(f"Error opening directory: {str(e)}")
