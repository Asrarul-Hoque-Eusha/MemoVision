import { useState } from "react";
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperclip } from "@fortawesome/free-solid-svg-icons";

import api from "../api.js";
import NavBar from "./NavBar.jsx";


const ChatBot = () => {

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [answering, setAnswering] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if ((!inputText.trim() && !image)) {
            alert("Please enter a query or upload an image!");
            setErrorMessage("");
            return;
    }
    else if (errorMessage) {
        alert("Unsupported file type detected!");
        setErrorMessage("");
        return;
    }
    setAnswering(true)
    const formData = new FormData();
    if (inputText.trim()) {
        formData.append("query", inputText);
    }
    if (image) {
        formData.append("image", image);
    }
    try {
          const response = await api.post('/ask-query/', formData, {
              headers: {
                  'content-type': 'multipart/form-data'
              }
          });
          const { query, query_image, retrieved_image, answer } = response.data;
          console.log("response: ", response.data);
          setMessages([...messages,{
            query: query,
            image: query_image,
            retrieved_image: retrieved_image,
            answer: answer,
          }]);

          setInputText("");
          setImage(null);
          setPreview(null);
          setAnswering(false);
    }
    catch (error) {
      console.log(error);
      setMessages([...messages,{
            query: inputText,
            image: image,
            retrieved_image: [],
            answer: "The server is not responding now to the search request. Please try again.",
      }]);

      setInputText("");
      setImage(null);
      setPreview(null);
      setAnswering(false);
      setErrorMessage("");
    }

  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const allowedTypes = ["image/png", "image/jpeg", "image/webp"];
    if (file && allowedTypes.includes(file.type)) {
        setImage(file);
        const imageUrl = URL.createObjectURL(file); // Converting to temporary URL
        setPreview(imageUrl);
        setErrorMessage("")
    }
    else {
        setImage(null);
        setErrorMessage(`Unsupported file: ${file.name}`)
    }
  };


  return (
      <div className="bg-gray-800 min-h-screen">
          < NavBar />
          <div className="mx-10 pt-[85px] pb-28 h-auto text-white bg-gray-800">
            <h1 className="text-4xl my-2 text-center text-white font-bold">Chat</h1>
            <div className="min-h-[400px] h-auto mt-auto text-white
            items-center rounded shadow-md shadow-blue-300 mb-2 p-2 px-10">
                {messages.map((msg, index) => (
                  <div key={index} className="my-4 p-2 rounded h-auto bg-gray-700">
                      <div className="flex flex-col justify-end items-end bg-gray-500 ml-20 rounded-xl p-3 mb-2">

                        {msg.query && <p>{msg.query}</p>}
                        {msg.image && <img src={msg.image} alt="Uploaded" className="mt-2 w-[200px] h-auto rounded" />}
                      </div>

                      <div>
                        {msg.answer && <p>{msg.answer}</p>}
                        {msg.retrieved_image && (
                          <div className = "flex ">
                            {msg.retrieved_image.map((imgSrc, idx) => (
                                <div key={idx} className="flex flex-col retrieved-image-container">
                                    <Link to={`/image-viewer/${encodeURIComponent(imgSrc)}`} target="_blank"
                                          //state={{ imgSrc }}
                                    >
                                        <img
                                          src={imgSrc}
                                          alt={`Retrieved Image ${idx}`}
                                          className="w-[200px] h-[180px] rounded m-2"
                                        />
                                    </Link>
                                    <p className="text-white text-center">{idx+1}</p>
                                </div>
                              ))}
                            </div>
                        )}
                      </div>
                  </div>
                ))}
            </div>

            <div className="fixed bottom-0 min-h-[100px] h-auto inset-x-0 bg-gray-800 rounded-xl shadow-md
            shadow-sky-500 flex flex-col justify-center items-center p-2 w-[90%] mx-auto">
              <div className="flex items-center w-full gap-2 ">
                  {answering && (<p className="px-2">Answering...</p>)}
                  <input
                      type="text"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder="Type a query about image..."
                      className="flex-grow p-2 bg-gray-900 focus:outline-none rounded"
                  />
                  <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" id="fileInput"/>
                  <label htmlFor="fileInput" className="cursor-pointer flex items-center justify-center w-[50px] p-3 bg-gray-500 rounded">
                    <FontAwesomeIcon icon={faPaperclip}/>
                  </label>
                  <button onClick={handleSendMessage} className="p-2 bg-blue-400 hover:bg-blue-600 text-white rounded">
                    Ask
                  </button>
              </div>
              <div>
                {preview && (
                  <div className="mt-2">
                      <img src={preview} alt="Preview" className="w-[120px] h-auto rounded" />
                  </div>
                )}
                  {errorMessage && (<p className="text-red-700">{errorMessage}</p>)}
              </div>
            </div>
        </div>
      </div>
  );
}

export default ChatBot;