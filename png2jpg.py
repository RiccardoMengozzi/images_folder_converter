import os
import zipfile
from PIL import Image

def convert_and_zip(input_folder, output_zip):
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return

    temp_output_folder = "converted_images"

    # Ensure the temp folder exists
    if not os.path.exists(temp_output_folder):
        os.makedirs(temp_output_folder)

    for root, dirs, files in os.walk(input_folder):
        # Determine the relative path
        relative_path = os.path.relpath(root, input_folder)
        output_folder_path = os.path.join(temp_output_folder, relative_path)

        # Ensure the output folder exists
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        for file in files:
            if file.lower().endswith(".png"):
                input_file_path = os.path.join(root, file)
                output_file_name = os.path.splitext(file)[0] + ".jpg"
                output_file_path = os.path.join(output_folder_path, output_file_name)

                # Convert PNG to JPG
                try:
                    with Image.open(input_file_path) as img:
                        # Create a white background if the image has transparency
                        if img.mode in ("RGBA", "LA") or ("transparency" in img.info):
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[3] if "A" in img.mode else None)
                            background.save(output_file_path, "JPEG")
                        else:
                            rgb_img = img.convert("RGB")
                            rgb_img.save(output_file_path, "JPEG")
                except Exception as e:
                    print(f"Error converting {input_file_path}: {e}")

    # Create the zip file
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_output_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_output_folder)
                zipf.write(file_path, arcname)

    # Cleanup temporary folder
    for root, dirs, files in os.walk(temp_output_folder, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_output_folder)

if __name__ == "__main__":
    input_folder = os.path.expanduser("~/Desktop/Figures")  # Input folder containing subfolders and .png images
    output_zip = os.path.expanduser("~/Desktop/converted_images.zip")  # Output zip file

    convert_and_zip(input_folder, output_zip)
    print(f"All images converted and saved to {output_zip}")
