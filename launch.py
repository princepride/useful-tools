import gradio as gr
from file_tools import folder_scan, export_pdf_text
from image_tools import image_convert

def update_image_size(use_scale, scale, image_width, image_height):
    if use_scale:
        width = int(image_width * scale)
        height = int(image_height * scale)
    else:
        width, height = None, None
    return width, height

with gr.Blocks() as iface:
    with gr.Tab("File"):
        with gr.Accordion("Folder Scan"):
            gr.Markdown("Scan folders and list their contents. Enter multiple paths, one per line. Optionally, specify patterns to ignore (one per line) and choose to print file content.")
            with gr.Row():
                paths_input = gr.Textbox(lines=5, label="Folders paths", placeholder="Enter paths, one per line")
                ignore_patterns_input = gr.Textbox(lines=5, label="Ignore patterns", placeholder="Enter ignore patterns, one per line")
            with gr.Row():
                save_to_file_checkbox = gr.Checkbox(label="Save to file")
                print_file_name_checkbox = gr.Checkbox(label="Print file name")
                print_file_content_checkbox = gr.Checkbox(label="Print file content")
            scan_button = gr.Button("Scan Folders")
            scan_output = gr.Textbox(label="Output", show_copy_button=True)
            scan_button.click(
                fn=folder_scan,
                inputs=[
                    paths_input,
                    ignore_patterns_input,
                    save_to_file_checkbox,
                    print_file_content_checkbox,
                    print_file_name_checkbox
                ],
                outputs=scan_output
            )

        with gr.Accordion("Export PDF Text"):
            gr.Markdown("Export text content from PDF files.")
            pdf_paths_input = gr.Textbox(lines=5, placeholder="Enter PDF file paths, one per line")
            export_pdf_button = gr.Button("Export PDF Text")
            pdf_text_output = gr.Textbox(label="Output", show_copy_button=True)
            export_pdf_button.click(
                fn=export_pdf_text,
                inputs=pdf_paths_input,
                outputs=pdf_text_output
            )

    with gr.Tab("Image"):
        with gr.Accordion("Image Convert"):
            gr.Markdown("Convert images to specified size and format.")
            with gr.Row():
                image_paths = gr.Textbox(lines=5, placeholder="Enter image paths, one per line")
            with gr.Column():
                use_scale_checkbox = gr.Checkbox(label="Use scale", value=True)
                scale_input = gr.Number(label="Scale", value=1.0)
            with gr.Row():
                width_input = gr.Number(label="Width", interactive=False)
                height_input = gr.Number(label="Height", interactive=False)
            image_format = gr.Radio(["jpg", "png", "bmp"], label="Target format", value="jpg")
            image_width_input = gr.Number(label="Image Width", visible=False, value=800)
            image_height_input = gr.Number(label="Image Height", visible=False, value=600)
            convert_button = gr.Button("Convert Images")
            image_output = gr.Textbox(label="Output")
            convert_button.click(
                fn=image_convert,
                inputs=[
                    image_paths,
                    scale_input,
                    width_input,
                    height_input,
                    image_format
                ],
                outputs=image_output
            )
            use_scale_checkbox.change(
                fn=update_image_size,
                inputs=[use_scale_checkbox, scale_input, image_width_input, image_height_input],
                outputs=[width_input, height_input]
            )

iface.launch(debug=True)