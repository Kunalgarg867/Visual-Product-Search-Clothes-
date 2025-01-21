import React, { useState ,useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [queryImage, setQueryImage] = useState(null);
  const [similarImages, setSimilarImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (e) => {
    setQueryImage(e.target.files[0]);
  };


  const handleSearch = async () => {
    if (!queryImage) {
      alert("Please upload an image first.");
      return;
    }

    setLoading(true);
    setSimilarImages([]);

    const formData = new FormData();
    formData.append("file", queryImage);

    try {
      const response = await axios.post("http://localhost:8000/find-similar-images", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSimilarImages(response.data.similar_images);
    } catch (error) {
      console.error("Error finding similar images:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="body">
      <div className="App">
        <h1>The Cloth Store</h1>
        <div className="upload-section">
          <input type="file" accept="image/*" onChange={handleImageUpload} />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Searching..." : "Find Similar Images"}
          </button>
        </div>
        {queryImage && (
          <div className="preview">
            <h3>Uploaded Image:</h3>
            <img src={URL.createObjectURL(queryImage)} alt="Uploaded Query" />
          </div>
        )}
        {similarImages.length > 0 && (
          <div className="results">
            <h3>Similar Images:</h3>
            <div className="image-grid">
              {similarImages.map((img, index) => (
                <div key={index} className="image-item">
                  <img src={`public/dataset/${img.slice(0, img.length-4)}.jpg`} alt={`Similar ${index + 1}`} />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
