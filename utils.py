from pathlib import Path
from PIL import Image

def convert_jpg_to_webp(input_dir,  output_dir, quality: int = 80):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    successful_conversions = 0
    failed_conversions = 0
    
    for input_path in input_dir.glob('*.jpg'):
        try:
            with Image.open(input_path) as img:
                output_path = output_dir / (input_path.stem + '.webp')
                
                img.save(output_path, 'WEBP', quality=quality)
            
            successful_conversions += 1
            print(f"Converted: {input_path.name} -> {output_path.name}")
        
        except Exception as e:
            failed_conversions += 1
            print(f"Error converting {input_path.name}: {e}")
    
    # Print summary
    print("\nConversion Summary:")
    print(f"Total images converted: {successful_conversions}")
    print(f"Failed conversions: {failed_conversions}")

if __name__ == "__main__":
    in_dir = Path('web/app/static/images/patches')
    out_dir = Path('web/app/static/images/patches_webp')

    convert_jpg_to_webp(in_dir, out_dir)

