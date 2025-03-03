import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import api from '../api.js';
import Navbar from "./NavBar.jsx";

const Gallery = () => {

    const [images, setImages] = useState([]);
    const fetchItems = async () => {
        try {
            const response = await api.get('/gallery/');
            console.log(response.data);
            if (Array.isArray(response.data)){
                console.log("array");
            }
            const {images} = response.data
            console.log(images);
            setImages(images)
        }
        catch (error) {
            console.log("Error loading files:", error);
        }
    };

    useEffect(() => {
        fetchItems();
        }, []);

    return (
        <div className="bg-gray-800 h-auto min-h-screen">
            <Navbar />
            <div className='pt-[90px]'>
                <h1 className="font-bold text-4xl text-white text-center my-5">Gallery</h1>
                <div className="mx-10 py-5">
                    {images.length === 0 && (
                        <div className="mx-10 h-[400px] flex items-center justify-center">
                            <p className=" text-center text-white text-2xl">
                                No Images in the gallery or Internal Server Error.
                            </p>
                        </div>
                    )}
                    <div className="flex flex-wrap justify-center gap-4">
                        { images.map((imgSrc, idx) => (
                            <Link key={idx} to={`/image-viewer/${encodeURIComponent(imgSrc)}`}
                                  target="_blank"
                                  //to = "/view" state={{ imgSrc }}
                            >
                                <img
                                    //key={idx}
                                    src={imgSrc}
                                    alt={`Uploaded Image ${idx}`}
                                    className="w-[200px] h-[180px] rounded shadow-lg"
                                />
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Gallery;