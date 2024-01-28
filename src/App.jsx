import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const routes = ["http://127.0.0.1:5000/", "http://127.0.0.1:5000/add-input"];
  const [file, setFile] = useState(null);
  const [downloadFile, setDownloadFile] = useState(null);

  const handleFile = async (event) => {
    const eFile = event.target.files[0];
    setFile(eFile);
  };

  const handleUpload = async () => {
    if (file) {
      const outputDiv = document.getElementById("output");
      const formData = new FormData();
      formData.append("file", file);
      await axios
        .post(routes[1], formData, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          setDownloadFile(response.data);
          outputDiv.innerHTML = `<p>File uploaded successfully.</p>`;
        })
        .catch((error) => {
          console.error("Error:", error);
          outputDiv.innerHTML =
            "<p>Error uploading file. Please try again.</p>";
        });
    }
  };

  const handleDownload = () => {
    // Create a Blob from the PDF data
    const blob = new Blob([downloadFile], { type: "application/pdf" });
    // Create a temporary link and trigger the download
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "downloaded_file.pdf";
    link.click();
  };

  return (
    <>
      <div className="body-style">
        <div className="div-1">
          <h1>Upload Pdf File</h1>
        </div>
        <div id="uploadForm" className="div-2">
          <input onChange={handleFile} id="fileInput" type="file" name="file" />
          <div className="div-3">
            <button onClick={() => handleUpload()} className="btn-1">
              Upload
            </button>
            <button
              onClick={() => handleDownload()}
              disabled={downloadFile === null ? true : false}
              className="btn-2"
            >
              Download
            </button>

            <button
              onClick={() => {
                setDownloadFile(null);
                setFile(null);
                const fileDiv = document.getElementById("fileInput");
                fileDiv.value = "";
              }}
              className="btn-3"
            >
              Clear
            </button>
          </div>
        </div>
        <div id="output"></div>
      </div>
    </>
  );
}

export default App;
