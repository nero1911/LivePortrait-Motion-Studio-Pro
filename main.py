import gradio as gr
import numpy as np
from PIL import Image
import cv2
import os
import torch
from datetime import datetime
import threading
import time
from pathlib import Path
import logging

from animation_engine import AnimationEngine
from ui_handler import UIHandler
from expression_presets import ExpressionPresets

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LivePortraitStudio:
    def __init__(self):
        logger.info("Initializing LivePortrait Motion Studio Pro...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        self.animation_engine = AnimationEngine(device=self.device)
        self.ui_handler = UIHandler()
        self.expression_presets = ExpressionPresets()
        
        self.current_image = None
        self.current_animation_params = {}
        self.preview_queue = []
        self.is_generating = False
        self.debounce_timer = None
        self.last_generation_time = 0
        self.preview_cache = {}
        
        logger.info("Initialization complete")
    
    def upload_image(self, image_file):
        """Handle image upload"""
        try:
            if image_file is None:
                return None, "No image selected"
            
            logger.info(f"Uploading image: {image_file.name}")
            
            img = Image.open(image_file)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Validate image dimensions
            if img.size[0] < 256 or img.size[1] < 256:
                return None, "Image too small (minimum 256x256)"
            
            if img.size[0] > 1920 or img.size[1] > 1920:
                # Resize if too large
                img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
            
            self.current_image = img
            self.preview_cache = {}
            
            logger.info(f"Image uploaded successfully: {img.size}")
            return img, "Image loaded successfully"
        
        except Exception as e:
            logger.error(f"Image upload error: {str(e)}")
            return None, f"Error: {str(e)}"
    
    def apply_expression_preset(self, preset_name):
        """Apply expression preset"""
        try:
            logger.info(f"Applying expression preset: {preset_name}")
            preset_values = self.expression_presets.get_preset(preset_name)
            
            if preset_values is None:
                return "Preset not found"
            
            return preset_values, f"Preset '{preset_name}' applied"
        
        except Exception as e:
            logger.error(f"Preset error: {str(e)}")
            return None, f"Error: {str(e)}"
    
    def update_animation_params(self, **params):
        """Update animation parameters with debouncing"""
        self.current_animation_params = params
        
        # Clear previous timer
        if self.debounce_timer is not None:
            self.debounce_timer.cancel()
        
        # Set new timer for 0.5 seconds
        self.debounce_timer = threading.Timer(
            0.5,
            self._generate_preview
        )
        self.debounce_timer.daemon = True
        self.debounce_timer.start()
    
    def _generate_preview(self):
        """Generate preview with debouncing"""
        if self.current_image is None:
            return None, "No image loaded"
        
        if self.is_generating:
            return None, "Already generating..."
        
        try:
            self.is_generating = True
            logger.info("Generating preview...")
            
            # Generate animation
            video_frames = self.animation_engine.generate_animation(
                self.current_image,
                **self.current_animation_params,
                preview_mode=True
            )
            
            if video_frames is None:
                return None, "Animation generation failed"
            
            # Create preview video
            preview_path = self.ui_handler.create_preview_video(
                video_frames,
                fps=15
            )
            
            logger.info(f"Preview generated: {preview_path}")
            return preview_path, "Preview updated"
        
        except Exception as e:
            logger.error(f"Preview generation error: {str(e)}")
            return None, f"Error: {str(e)}"
        
        finally:
            self.is_generating = False
    
    def render_final_video(self, output_format, fps, duration, resolution):
        """Render final video with user settings"""
        if self.current_image is None:
            return None, "No image loaded"
        
        try:
            logger.info(f"Starting final render: {output_format} {resolution}p {fps}fps {duration}s")
            
            # Map resolution
            res_map = {
                "480P": (854, 480),
                "720P": (1280, 720),
                "1080P": (1920, 1080)
            }
            
            output_size = res_map.get(resolution, (854, 480))
            
            # Generate high-quality animation
            video_frames = self.animation_engine.generate_animation(
                self.current_image,
                **self.current_animation_params,
                preview_mode=False,
                duration=duration,
                fps=fps
            )
            
            if video_frames is None:
                return None, "Animation generation failed"
            
            # Save video
            output_path = self.ui_handler.save_video(
                video_frames,
                output_format=output_format,
                fps=fps,
                output_size=output_size
            )
            
            logger.info(f"Video saved: {output_path}")
            return output_path, f"Saved successfully: {output_path}"
        
        except Exception as e:
            logger.error(f"Render error: {str(e)}")
            return None, f"Error: {str(e)}"
    
    def create_ui(self):
        """Create Gradio UI"""
        logger.info("Creating UI...")
        
        with gr.Blocks(title="LivePortrait Motion Studio Pro") as demo:
            gr.Markdown("# 🎬 LivePortrait Motion Studio Pro")
            gr.Markdown("*Real-time Interactive Animation Editor*")
            
            with gr.Row():
                # Left Panel - Controls
                with gr.Column(scale=1):
                    gr.Markdown("### 📤 Image Upload")
                    image_input = gr.File(
                        label="Upload Image (PNG/JPG/WEBP)",
                        type="filepath",
                        file_types=[".png", ".jpg", ".jpeg", ".webp"]
                    )
                    image_display = gr.Image(label="Preview", type="pil")
                    upload_status = gr.Textbox(
                        label="Status",
                        value="Ready",
                        interactive=False
                    )
                    
                    gr.Markdown("### 🎭 Expression Presets")
                    preset_select = gr.Dropdown(
                        label="Select Preset",
                        choices=self.expression_presets.get_preset_names(),
                        value="Neutral"
                    )
                    preset_button = gr.Button("Apply Preset", variant="primary")
                    
                    gr.Markdown("### 🎨 Animation Controls")
                    
                    # Facial Animation Controls
                    gr.Markdown("#### 👤 Face Animation")
                    blink_intensity = gr.Slider(
                        label="👀 Eye Blink Intensity",
                        minimum=0, maximum=100, value=50, step=5
                    )
                    blink_frequency = gr.Slider(
                        label="👁️ Eye Blink Frequency",
                        minimum=0.1, maximum=5, value=1, step=0.1
                    )
                    
                    smile_strength = gr.Slider(
                        label="😊 Smile Strength",
                        minimum=0, maximum=100, value=30, step=5
                    )
                    expression_intensity = gr.Slider(
                        label="😐 Expression Intensity",
                        minimum=0, maximum=100, value=50, step=5
                    )
                    
                    # Head Movement Controls
                    gr.Markdown("#### 🤨 Head Movement")
                    head_yaw = gr.Slider(
                        label="↔️ Head Yaw (Left/Right)",
                        minimum=-30, maximum=30, value=0, step=2
                    )
                    head_pitch = gr.Slider(
                        label="↕️ Head Pitch (Up/Down)",
                        minimum=-30, maximum=30, value=0, step=2
                    )
                    head_roll = gr.Slider(
                        label="⤴️ Head Roll (Tilt)",
                        minimum=-20, maximum=20, value=0, step=2
                    )
                    head_nod_intensity = gr.Slider(
                        label="🤔 Head Nod Intensity",
                        minimum=0, maximum=100, value=30, step=5
                    )
                    
                    # Hair and Breath Controls
                    gr.Markdown("#### 💨 Physics Simulation")
                    hair_flutter = gr.Slider(
                        label="💇 Hair Flutter Amount",
                        minimum=0, maximum=100, value=20, step=5
                    )
                    hair_direction = gr.Slider(
                        label="🌬️ Hair Wind Direction",
                        minimum=-180, maximum=180, value=0, step=15
                    )
                    breathing_intensity = gr.Slider(
                        label="💓 Breathing Intensity",
                        minimum=0, maximum=100, value=30, step=5
                    )
                    breathing_frequency = gr.Slider(
                        label="❤️ Breathing Frequency",
                        minimum=0.1, maximum=2, value=0.5, step=0.1
                    )
                    
                    # Advanced Controls
                    gr.Markdown("#### 👁️ Eye Gaze")
                    eye_gaze_x = gr.Slider(
                        label="👁️ Eye Gaze X (Left/Right)",
                        minimum=-30, maximum=30, value=0, step=5
                    )
                    eye_gaze_y = gr.Slider(
                        label="👁️ Eye Gaze Y (Up/Down)",
                        minimum=-30, maximum=30, value=0, step=5
                    )
                    
                    # Output Settings
                    gr.Markdown("### ⚙️ Output Settings")
                    gr.Markdown("**Video Format**")
                    output_format = gr.Radio(
                        label="Format",
                        choices=["MP4", "GIF"],
                        value="MP4"
                    )
                    fps = gr.Slider(
                        label="FPS",
                        minimum=15, maximum=60, value=30, step=5
                    )
                    duration = gr.Slider(
                        label="Duration (seconds)",
                        minimum=1, maximum=10, value=3, step=0.5
                    )
                    resolution = gr.Radio(
                        label="Resolution",
                        choices=["480P", "720P", "1080P"],
                        value="480P"
                    )
                    
                    render_button = gr.Button("🎬 Render & Save", variant="primary", size="lg")
                
                # Right Panel - Preview
                with gr.Column(scale=1):
                    gr.Markdown("### 📹 Live Preview")
                    preview_video = gr.Video(
                        label="Animation Preview",
                        format="mp4"
                    )
                    preview_status = gr.Textbox(
                        label="Preview Status",
                        value="Waiting for input...",
                        interactive=False
                    )
                    
                    gr.Markdown("### 📋 Generation Log")
                    log_output = gr.Textbox(
                        label="Log",
                        lines=15,
                        max_lines=20,
                        interactive=False,
                        value="App started...\n"
                    )
            
            # Event handlers
            def on_image_upload(file):
                result, status = self.upload_image(file)
                return result, status
            
            def on_slider_change(**kwargs):
                self.update_animation_params(**kwargs)
                return "Preview generating... (0.5s delay)"
            
            def on_preset_apply():
                preset_values, status = self.apply_expression_preset(preset_select.value)
                if preset_values:
                    return (
                        preset_values.get('smile_strength', 30),
                        preset_values.get('expression_intensity', 50),
                        preset_values.get('head_yaw', 0),
                        preset_values.get('head_pitch', 0),
                        preset_values.get('head_nod_intensity', 30),
                        status
                    )
                return 30, 50, 0, 0, 30, status
            
            def on_render(**kwargs):
                output_path, status = self.render_final_video(
                    kwargs['output_format'],
                    int(kwargs['fps']),
                    kwargs['duration'],
                    kwargs['resolution']
                )
                return output_path, status
            
            image_input.change(
                on_image_upload,
                inputs=[image_input],
                outputs=[image_display, upload_status]
            )
            
            # Connect all sliders to debounced update
            sliders = [
                blink_intensity, blink_frequency, smile_strength, expression_intensity,
                head_yaw, head_pitch, head_roll, head_nod_intensity,
                hair_flutter, hair_direction, breathing_intensity, breathing_frequency,
                eye_gaze_x, eye_gaze_y
            ]
            
            for slider in sliders:
                slider.change(
                    on_slider_change,
                    inputs=sliders,
                    outputs=[preview_status]
                )
            
            preset_button.click(
                on_preset_apply,
                outputs=[smile_strength, expression_intensity, head_yaw, head_pitch, head_nod_intensity, upload_status]
            )
            
            render_button.click(
                on_render,
                inputs=[output_format, fps, duration, resolution],
                outputs=[preview_video, log_output]
            )
        
        return demo

def main():
    studio = LivePortraitStudio()
    demo = studio.create_ui()
    
    logger.info("Launching Gradio interface...")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
