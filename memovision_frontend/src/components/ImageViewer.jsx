import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";

import api from "../api.js";
import Logo from '../assets/logo.jpg';
import NavBar from "./NavBar.jsx";

const ImageViewer = () => {

    const { filepath } = useParams(); // Extracting filename from URL
    const imgSrc = decodeURIComponent(filepath); // Decoding back
    const decodedFilepath = imgSrc.replace("http://localhost:8000","");
    const [imageDetails, setImageDetails] = useState(null);
    const [error, setError] = useState(null);
    console.log(decodedFilepath)
    console.log(imgSrc)
    useEffect(() => {
        //if (!imgSrc) return; // No need to fetch if no image source

        const fetchImageDetails = async () => {
            try {
                const response = await api.get(`/image-viewer/${encodeURIComponent(decodedFilepath)}`);
                //,  {    params: { filepath: imgSrc } }
                const {descriptions, tags} = response.data
                setImageDetails(response.data);
                console.log(descriptions)
                console.log(tags)
                console.log(response.data)
            } catch (err) {
                setError(err.response?.data?.message || "Failed to fetch image details");
            }
        };
        fetchImageDetails();
    }, [decodedFilepath]);


    return (
        <div className="bg-gray-800 h-auto min-h-screen">
            < NavBar />
            <div className="p-10 pt-[90px] text-white items-center justify-center">
                <h1 className="font-bold text-4xl text-center mb-10">Image Viewer</h1>
                {(!imgSrc || imgSrc === ":filepath") && (
                    <div className="flex flex-col m-20 items-center justify-center gap-5">
                        <p className="text-5xl text-white font-bold">404</p>
                        <p className="text-2xl text-white font-bold">Image Not Available</p>
                        <img className="h-[200px] w-auto" src={Logo} alt="Dummy"/>
                    </div>
                )}
                {(imgSrc !== ":filepath") && (
                    <div className="flex items-center gap-5">
                        <img className="h-[400px] max-w-[800px] rounded shadow-lg" src={imgSrc} alt="Selected Image"/>
                        <div className="p-4 bg-gray-700 shadow-md shadow-sky-500 rounded-lg w-full max-w-2xl">
                            <h2 className="text-xl font-bold mb-2">Image Details</h2>
                            {error ? (
                                <p className="text-orange-700">{error}</p>
                            ) : (
                                <>
                                    <p className="py-2">
                                        <strong className="text-lg">Description:</strong> {imageDetails?.descriptions || "No description available"}
                                    </p>
                                    <p className="pb-2"><strong className="text-lg">Tags:</strong> {imageDetails?.tags || "No tags available"}
                                    </p>
                                </>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default ImageViewer;