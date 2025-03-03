import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import HomePage from "./Components/HomePage.jsx";
import NavBar from "./Components/NavBar.jsx";
import BatchUploader from "./Components/BatchUploader.jsx";
import ChatBot from "./Components/ChatBot.jsx";
import Gallery from "./Components/Gallery.jsx";
import ImageViewer from "./Components/ImageViewer.jsx";

function App() {
  return (
      <Router>
          <Routes>
              <Route path = "/" element={<HomePage />} />
              <Route path = "/gallery" element={<Gallery />} />
              <Route path = "/chat" element={<ChatBot />} />
              <Route path = "/upload" element={<BatchUploader />} />
              <Route path = "/image-viewer/:filepath" element={<ImageViewer />} />
          </Routes>
      </Router>
  )
}

export default App
