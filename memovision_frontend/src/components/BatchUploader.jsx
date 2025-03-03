import { useState, useEffect } from "react";
import api from "../api";
import {faUpload} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Navbar from "./NavBar.jsx";


const BatchUploader = () => {

    const [files, setFiles] = useState([]);
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [dots, setDots] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [messages, setMessages] = useState({});
    const [showPopup, setShowPopup] = useState(false);
    const imageLimit = 300;

    useEffect(() => {
        if (!loading) return;

        const interval = setInterval(() => {
          setDots((prev) => (prev.length < 3 ? prev + "." : ""));
        }, 500);

        return () => clearInterval(interval);
        }, [loading]
    );

    useEffect(() => {
        if (messages.message && !loading) {
            setShowPopup(true);

            const timer = setTimeout(() => {
                setShowPopup(false);
            }, 10000); // 10 seconds

            return () => clearTimeout(timer);
        }
    }, [messages, loading]);

    const handleChange = (event) => {
        const selectedFiles = Array.from(event.target.files);
        const allowedTypes = ["image/png", "image/jpeg", "image/webp"];
        const validFiles = selectedFiles.filter(file => allowedTypes.includes(file.type));
        const invalidFiles = selectedFiles.filter(file => !allowedTypes.includes(file.type));

        if (invalidFiles.length > 0) {
            setErrorMessage(`Unsupported file(s): ${invalidFiles.map(file => file.name).join(", ")}`);
        } else {
            setErrorMessage(""); // Clear error if all files are valid
        }
        setFiles(validFiles);
        setImages(validFiles.map(file => URL.createObjectURL(file)));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();
        if (files.length === 0) {
            alert("Please select (supported) files to upload!");
            return;
        }
        else if (files.length > imageLimit){
            alert(`Please select files less than ${imageLimit}!`);
            return;
        }
        setLoading(true)
        const formData = new FormData();
        files.forEach((file) => {
            formData.append("files", file); // "files" must match FastAPI parameter
        });

        try {
            const response = await api.post('/batch-upload/', formData, {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            });
            const { upload_message, file_exists } = response.data;
            setMessages({
                message: upload_message,
                exists: file_exists,
            })
            console.log(files);
            setFiles([]);
            setImages([]);
            setLoading(false);
        }
        catch (error) {
            console.log("Error uploading files:", error);
            setLoading(false);
            setMessages({
                message: "Error uploading files. Please try again.",
                exists: []
            });
            setErrorMessage("");
        }
    }

    return (
        <div className="bg-gray-800 h-auto min-h-screen">
            <Navbar />
            <div className="pt-[85px] p-10 text-white">
                <h1 className="mb-10  text-center text-3xl font-bold">Batch Image Uploader</h1>
                <div className="bg-gray-700 py-8 shadow-md rounded-md shadow-sky-500">
                    {images.length === 0 && (<div className="h-[250px]  bg-center bg-contain bg-no-repeat
                      bg-[url(/public/upload_icon.png)] "></div>)}
                    <div className="mx-20 mt-5">
                        <form className="flex flex-col items-center gap-6" onSubmit={handleSubmit}>
                            {/*<label className="font-bold"> Upload Image: </label>*/}
                            <input type="file" accept=".png, .jpg, .jpeg, .webp" className="hidden" multiple onChange={handleChange} name="files" id="filesInput"/>
                            <label htmlFor="filesInput" className="cursor-pointer py-3 px-5 duration-300
                             bg-blue-400 hover:bg-blue-600 rounded-md">
                                <FontAwesomeIcon icon={faUpload}/>
                                <span className="text-white font-bold mx-2">Select Files</span>
                            </label>
                            {loading && (<p className="mt-1 font-bold text-center text-xl">Uploading {files.length} Images{dots}</p>)}
                            {errorMessage && (<p className="text-red-700">{errorMessage}</p>)}
                            {images && (
                                <div className="grid grid-cols-6 mt-6">
                                    {images.map((image, index) => (
                                        <div key={index} className="col-span-1 m-2">
                                        <img alt={`image ${index}`} src={image} className='w-[150px] h-[130px]'/>
                                        </div>
                                    ))}
                                </div>
                            )}
                            <input type="submit" className="bg-blue-400 hover:bg-blue-600
                            w-[130px] font-bold rounded-md cursor-pointer
                            py-2 px-3 duration-300" value="Upload"/>
                        </form>
                    </div>

                    {showPopup && (
                    <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2
                    bg-gray-500 text-white p-6 rounded-lg shadow-lg z-50 max-w-md w-full">
                        <div className="text-center">
                            <h3 className="text-lg font-bold mb-4">Upload Status</h3>
                            <p className="mb-2">{messages.message}</p>
                            {messages.exists && messages.exists.length > 0 && (
                                <div className="mt-4">
                                    <p className="font-semibold">Files that already exist:</p>
                                    <ul className="text-left max-h-32 overflow-y-auto">
                                        {messages.exists.map((file, index) => (
                                            <li key={index} className="text-sm text-white">{file}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                            <button
                                onClick={() => setShowPopup(false)}
                                className="mt-6 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors duration-300"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                )}
                </div>
            </div>
        </div>
    );
}

export default BatchUploader;
