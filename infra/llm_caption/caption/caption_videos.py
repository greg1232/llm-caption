from openai import OpenAI

import os
import copy

from tqdm import tqdm

def caption_videos(images):
    for image in tqdm(images):
        if label_already_exists(image):
            continue

        caption = generate_caption(image)

        save_caption(image, caption)

def label_already_exists(image):
    label_path = get_label_path(image)

    return os.path.exists(label_path)

def caption_image(image):
    openai_api_key = "EMPTY"
    openai_api_base = "https://vllm.jasbrothers.com/v1"
    model_name = "Qwen/Qwen2-VL-7B-Instruct"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    def pil_to_base64(pil_image, format="PNG"):
        # Create an in-memory bytes buffer
        buffer = BytesIO()

        # Save the image to the buffer in the specified format
        pil_image.save(buffer, format=format)

        # Get the bytes from the buffer
        img_bytes = buffer.getvalue()

        # Encode the bytes as base64
        base64_encoded = base64.b64encode(img_bytes).decode('utf-8')

        return base64_encoded

    # Single-image input inference
    base64_string = pil_to_base64(image["image"], format="PNG")

    # If you want to create a data URL for embedding in HTML
    image_url = f"data:image/png;base64,{base64_string}"

    chat_response = client.chat.completions.create(
        model=model_name,
        messages=[{
            "role": "user",
            "content": [
                # NOTE: The prompt formatting with the image token `<image>` is not needed
                # since the prompt will be processed automatically by the API server.
                {"type": "text", "text": "What’s in this image?"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }],
    )

    return chat_response.choices[0].message.content

def get_label_path(image):
    base_path = "/app/llm_caption/data/labels"

    video_name = image["metadata"]["video_id"]
    frame_number = image["metadata"]["frame_number"]

    label_path = os.path.join(base_path, video_name, f"{frame_number}.json")

    return label_path

def save_caption(image, caption):
    label_path = get_label_path(image)

    os.makedirs(os.path.dirname(label_path), exist_ok=True)

    metadata = copy.deepcopy(image["metadata"])

    metadata["caption"] = caption

    with open(label_path, "w") as f:
        f.write(json.dumps(metadata, indent=4))


