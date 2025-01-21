from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from embedding import get_embedding 
from PIL import Image
import os
import numpy as np
from scipy.spatial.distance import cosine

app = FastAPI()

# Add CORS middleware to allow all origins (use carefully for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, you can specify specific URLs here for more security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Directory to save uploaded images temporarily
TEMP_IMAGE_DIR = "./temp_images"
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

# Load image embeddings from the file
EMBEDDINGS_FILE = "image_embeddings_dict.npy"
if not os.path.exists(EMBEDDINGS_FILE):
    raise FileNotFoundError(f"Embeddings file '{EMBEDDINGS_FILE}' not found.")
image_embeddings_dict = np.load(EMBEDDINGS_FILE, allow_pickle=True).item()

# Function to find the top 5 most similar images from the embeddings file
def find_similar_images(input_embedding, top_k=5):
    similarities = []

    # Compute cosine similarity for each image
    for image_name, embedding in image_embeddings_dict.items():
        similarity = 1 - cosine(input_embedding, embedding)
        similarities.append((image_name, similarity))

    # Sort by similarity (higher is better) and return the top_k
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    names = [sim[0] for sim in similarities]
    return names[:top_k]

# API endpoint to receive the image and return similar images
@app.post("/find-similar-images")
async def find_similar_images_endpoint(file: UploadFile):
    # Open the uploaded image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Save the uploaded image to a temporary directory
    temp_image_path = os.path.join(TEMP_IMAGE_DIR, file.filename)
    with open(temp_image_path, "wb") as f:
        f.write(await file.read())

    # Generate the embedding for the uploaded image
    embedding = get_embedding(temp_image_path)

    # Clean up: Remove the temporary image
    os.remove(temp_image_path)

    # Convert the embedding to a list (to make it JSON serializable)
    embedding_list = embedding.tolist()

    # Find similar images from the embeddings dictionary
    top_similar_images = find_similar_images(embedding_list)

    # Return the top 5 similar images and their similarity scores
    return {"similar_images": top_similar_images}
