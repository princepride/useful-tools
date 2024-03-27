import gradio as gr
from file_tools import folder_scan

iface = gr.Interface(
    fn=folder_scan,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter paths, one per line"),
        gr.Textbox(lines=2, placeholder="Enter ignore patterns, one per line"),
        gr.Checkbox(label="Save to file"),
        gr.Checkbox(label="Print file content")
    ],
    outputs="text",
    title="Folder Scanner",
    description="Scan folders and list their contents. Enter multiple paths separated by ';'. Optionally, specify patterns to ignore (one per line) and choose to print file content."
)

iface.launch(debug=True)