"""CAPTCHA generation and validation utilities."""

import random
import string
from io import BytesIO

from flask import session
from PIL import Image, ImageDraw, ImageFont


def generate_captcha():
    """
    Generate a random 4-character CAPTCHA image using PIL.

    Stores the answer in Flask session and returns image bytes.

    Returns:
        bytes: CAPTCHA image in PNG format
    """
    # Generate random 4-character string
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # Store in session
    session['captcha_answer'] = captcha_text

    # Create image
    width, height = 200, 60
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Draw some noise lines
    for _ in range(random.randint(3, 5)):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill='gray', width=1)

    # Draw text
    try:
        # Try to use a default font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 36)
    except (OSError, IOError):
        # Use default font if arial.ttf not found
        font = ImageFont.load_default()

    # Calculate text position
    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), captcha_text, fill='black', font=font)

    # Convert to bytes
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io.getvalue()


def validate_captcha(user_answer):
    """
    Validate user input against session stored CAPTCHA answer.

    Clears session on success/failure.

    Args:
        user_answer (str): User's CAPTCHA input

    Returns:
        bool: True if validation successful, False otherwise
    """
    stored_answer = session.get('captcha_answer', None)

    # Check if answer matches (case-insensitive)
    is_valid = stored_answer and user_answer.upper() == stored_answer.upper()

    # Clear session regardless
    if 'captcha_answer' in session:
        del session['captcha_answer']

    return is_valid
