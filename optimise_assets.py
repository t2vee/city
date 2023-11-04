import os
from PIL import Image
import cairosvg


def optimize_images(directory, output_directory=None):
    if output_directory is None:
        output_directory = directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        try:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico')):
                file_path = os.path.join(directory, filename)
                file_name, file_extension = os.path.splitext(filename)
                optimized_filename = file_name + '_optimised.webp'
                optimized_file_path = os.path.join(output_directory, optimized_filename)

                # Skip if the optimized file already exists
                if os.path.exists(optimized_file_path):
                    print(f'Skipping already optimised file: {optimized_filename}')
                    continue

                # Handle SVG and ICO separately
                if file_extension.lower() in ['.svg', '.ico']:
                    # Catch parsing errors for SVG files
                    try:
                        cairosvg.svg2png(url=file_path, write_to=file_path + '.png')
                        file_path += '.png'
                        file_extension = '.png'
                    except Exception as e:
                        print(f'Error converting {filename}: {e}')
                        continue

                # Open the image file
                with Image.open(file_path) as img:
                    # Convert non-WebP images to WebP, and optimize if it's already WebP
                    if file_extension.lower() != '.webp' or (
                            file_extension.lower() == '.webp' and 'optimised' not in file_name):
                        # Resize logic (if needed)
                        # Example: img = img.resize((new_width, new_height), Image.ANTIALIAS)

                        # Reduce quality and save
                        img.save(optimized_file_path, 'WEBP', quality=80)

                # Remove temporary PNG if created from SVG or ICO
                if file_extension.lower() in ['.svg', '.ico']:
                    os.remove(file_path)

                print(f'Processed and saved: {optimized_filename}')
        except Exception as e:
            print(f'Failed to process {filename}: {e}')

# Call the function with the directory of images
optimize_images(r'O:\usercontent\PYCHARMPROJECTS\Cityv2\res\CDN', r'O:\usercontent\PYCHARMPROJECTS\Cityv2\res\CDN\OPTIMISED')
