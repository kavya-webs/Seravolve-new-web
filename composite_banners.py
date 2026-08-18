from PIL import Image, ImageDraw, ImageFilter

def create_shadow(image, offset=(0, 10), radius=15, opacity=120):
    """Create a soft shadow for the given RGBA image."""
    shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    shadow_mask = image.split()[3]
    
    shadow_draw = ImageDraw.Draw(shadow)
    shadow.paste((0, 0, 0, opacity), mask=shadow_mask)
    
    # Blur the shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius))
    return shadow

def composite_product(bg, product_path, position, target_height):
    """Resize product and paste it onto bg with a shadow at the specified position (x, y of bottom center)."""
    try:
        product = Image.open(product_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening {product_path}: {e}")
        return bg
        
    aspect_ratio = product.width / product.height
    new_width = int(target_height * aspect_ratio)
    product = product.resize((new_width, target_height), Image.LANCZOS)
    
    shadow = create_shadow(product, offset=(0, 10), radius=10, opacity=100)
    
    # Position is (x_center, y_bottom)
    x = position[0] - new_width // 2
    y = position[1] - target_height
    
    # Paste shadow with slight offset
    bg.paste(shadow, (x, y + 5), shadow)
    
    # Paste product
    bg.paste(product, (x, y), product)
    
    return bg

# --- Paths ---
workspace = "e:\\Seravolve-2"
assets = f"{workspace}\\assets"
mockups = f"{workspace}\\mockup"

# These paths are from the previous generation steps. I'll pass them in as arguments or hardcode them based on the variables.
import sys

bg1_path = sys.argv[1]
bg2_path = sys.argv[2]
bg3_path = sys.argv[3]

# --- Banner 1: Full Routine (5 products) ---
try:
    bg1 = Image.open(bg1_path).convert("RGBA")
    # Coordinates for the 5 pedestals in bg1 (approximate based on the generated image)
    # The image is 1024x576 (or similar 16:9 like 1344x768 or 1792x1024). Let's assume standard generate_image size which is 1792x1024.
    w, h = bg1.size
    print(f"BG1 size: {w}x{h}")
    
    # Assuming pedestals are distributed roughly from left to right.
    bg1 = composite_product(bg1, f"{mockups}\\4.png", (int(w*0.22), int(h*0.72)), int(h*0.45))
    bg1 = composite_product(bg1, f"{mockups}\\2.png", (int(w*0.37), int(h*0.74)), int(h*0.22))
    bg1 = composite_product(bg1, f"{mockups}\\3.png", (int(w*0.52), int(h*0.72)), int(h*0.55))
    bg1 = composite_product(bg1, f"{mockups}\\1.png", (int(w*0.68), int(h*0.73)), int(h*0.35))
    bg1 = composite_product(bg1, f"{mockups}\\5.png", (int(w*0.82), int(h*0.72)), int(h*0.48))

    bg1.save(f"{assets}\\hero-banner-1-full-routine.png")
    print("Saved Banner 1")
except Exception as e:
    print(f"Failed Banner 1: {e}")

# --- Banner 2: Why Seravolve (3 products on 5 clear pedestals) ---
try:
    bg2 = Image.open(bg2_path).convert("RGBA")
    w, h = bg2.size
    # There are 5 pedestals in this one too. We'll put 3 products in the center 3.
    bg2 = composite_product(bg2, f"{mockups}\\2.png", (int(w*0.35), int(h*0.62)), int(h*0.25))
    bg2 = composite_product(bg2, f"{mockups}\\1.png", (int(w*0.52), int(h*0.64)), int(h*0.40))
    bg2 = composite_product(bg2, f"{mockups}\\4.png", (int(w*0.69), int(h*0.61)), int(h*0.45))

    bg2.save(f"{assets}\\hero-banner-2-why-seravolve.png")
    print("Saved Banner 2")
except Exception as e:
    print(f"Failed Banner 2: {e}")


# --- Banner 3: Radiance Glow (3 products on 3 pedestals) ---
try:
    bg3 = Image.open(bg3_path).convert("RGBA")
    w, h = bg3.size
    
    bg3 = composite_product(bg3, f"{mockups}\\3.png", (int(w*0.25), int(h*0.62)), int(h*0.55))
    bg3 = composite_product(bg3, f"{mockups}\\1.png", (int(w*0.50), int(h*0.63)), int(h*0.35))
    bg3 = composite_product(bg3, f"{mockups}\\5.png", (int(w*0.77), int(h*0.62)), int(h*0.45))

    bg3.save(f"{assets}\\hero-banner-3-radiance-glow.png")
    print("Saved Banner 3")
except Exception as e:
    print(f"Failed Banner 3: {e}")
