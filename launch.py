import gradio as gr
from file_tools import folder_scan
from image_tools import image_convert

def update_image_size(proportional, width, height, image_width, image_height):
    if proportional:
        if width == 0:
            width = int(height * image_width / image_height)
        else:
            height = int(width * image_height / image_width)
    return width, height

with gr.Blocks() as iface:
    with gr.Tab("Folder Scan"):
        gr.Markdown("Scan folders and list their contents. Enter multiple paths, one per line. Optionally, specify patterns to ignore (one per line) and choose to print file content.")
        with gr.Row():
            paths_input = gr.Textbox(lines=5, placeholder="Enter paths, one per line")
            ignore_patterns_input = gr.Textbox(lines=5, placeholder="Enter ignore patterns, one per line")
        with gr.Row():
            save_to_file_checkbox = gr.Checkbox(label="Save to file")
            print_file_content_checkbox = gr.Checkbox(label="Print file content")
        scan_button = gr.Button("Scan Folders")
        scan_output = gr.Textbox(label="Output")
        
        scan_button.click(
            fn=folder_scan,
            inputs=[
                paths_input,
                ignore_patterns_input,
                save_to_file_checkbox,
                print_file_content_checkbox
            ],
            outputs=scan_output
        )
    
    with gr.Tab("Image Convert"):
        gr.Markdown("Convert images to specified size and format.")
        with gr.Row():
            image_paths = gr.Textbox(lines=5, placeholder="Enter image paths, one per line")
            with gr.Column():
                proportional_checkbox = gr.Checkbox(label="Keep proportional", value=True)
                with gr.Row():
                    width_input = gr.Number(label="Width", value=0)
                    height_input = gr.Number(label="Height", value=0)
                image_format = gr.Radio(["jpg", "png", "bmp"], label="Target format", value="jpg")
                image_width_input = gr.Number(label="Image Width", visible=False, value=800)
                image_height_input = gr.Number(label="Image Height", visible=False, value=600)
        convert_button = gr.Button("Convert Images")
        image_output = gr.Textbox(label="Output")
        
        convert_button.click(
            fn=image_convert,
            inputs=[
                image_paths,
                width_input,
                height_input,
                image_format
            ],
            outputs=image_output
        )
        
        proportional_checkbox.change(
            fn=update_image_size,
            inputs=[proportional_checkbox, width_input, height_input, image_width_input, image_height_input],
            outputs=[width_input, height_input]
        )

iface.launch(debug=True)