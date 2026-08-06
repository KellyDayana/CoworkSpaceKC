#!/usr/bin/env python3
"""
Script para crear iconos PWA placeholder
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Colores del proyecto
BG_COLOR = "#2D4A64"
TEXT_COLOR = "#FFFFFF"

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a tupla RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def crear_icono(size, output_path):
    """Crea un icono cuadrado con el texto KC"""
    # Crear imagen con fondo del color del proyecto
    img = Image.new('RGB', (size, size), hex_to_rgb(BG_COLOR))
    draw = ImageDraw.Draw(img)
    
    # Calcular tamaño de texto proporcional
    font_size = int(size * 0.4)
    
    # Intentar usar una fuente, si no está disponible usar la default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Texto a mostrar
    text = "KC"
    
    # Obtener dimensiones del texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calcular posición centrada
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Dibujar el texto
    draw.text((x, y), text, fill=hex_to_rgb(TEXT_COLOR), font=font)
    
    # Guardar la imagen
    img.save(output_path, 'PNG')
    print(f"✓ Icono creado: {output_path} ({size}x{size})")

# Crear directorio si no existe
os.makedirs('static/images', exist_ok=True)

# Crear iconos
crear_icono(192, 'static/images/icon-192.png')
crear_icono(512, 'static/images/icon-512.png')

print("\n✓ Iconos PWA creados exitosamente!")
print("Ahora puedes hacer commit y push a GitHub")
