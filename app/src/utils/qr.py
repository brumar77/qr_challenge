import qrcode
from PIL import Image
import os

def generate_qr_code(
    url: str, 
    color: str = "black", 
    size: int = 250, 
    output_dir: str = "static/qr_codes"):
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crear imagen
    img = qr.make_image(fill_color=color, back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    file_name = f"qr_{os.urandom(8).hex()}.png"
    file_path = os.path.join(output_dir, file_name)
    img.save(file_path)
    
    return file_path
