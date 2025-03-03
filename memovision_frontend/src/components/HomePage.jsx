import NavBar from './NavBar.jsx'
import Chatbot from '../../public/chatbot.png';
import Gallery from '../../public/gallery.png';
import Imageuploader from '../../public/image_uploader.png';
import Imageviewer from '../../public/image_viewer.png';

const HomePage = () =>  {
    const what = [
        {id: 1, text: 'AI-powered chatbot to retrieving photos.'},
        {id: 2, text: 'Allows to search images describing their content.'},
        {id: 3, text: 'Retrieves images based on text and visual similarities.'},
        {id: 4, text: 'Generate descriptions of uploaded images.'},
        {id: 5, text: 'Allows visual similarity search based on objects and composition.'},
        {id: 6, text: 'Automatically tag images with relevant keywords.'}
    ];
    const why = [
        {id: 1, text: 'Effortless Image Search – Find photos without browsing collections.'},
        {id: 2, text: 'Enhanced User Experience – Natural language-based search.'},
        {id: 3, text: 'Smart Organization – AI-generated tags help retrieve images.'},
        {id: 4, text: 'Context-Aware Retrieval – Understands contextual meaning.'},
        {id: 5, text: 'Multimodal Capabilities – Supports both text queries and image-based searches.'},
    ];
    const how = [
        {id: 1, text: 'Upload Images – Upload images using Image Uploader page.'},
        {id: 2, text: 'Search with Natural Language – Type queries like "Show me beach photos."'},
        {id: 3, text: 'Retrieve Relevant Images – Finds images using text and visual embeddings.'},
        {id: 4, text: 'View Image Descriptions – Click on image to see generated description.'},
        {id: 5, text: 'Find Similar Images – Select an image and retrieve visually similar ones.'},
    ];
    const data = [
    {
      component: "VLM Model",
      technology: "Llama 90B Vision (Preview) from Groq Cloud",
      reason: [
        "Supports multimodal inputs (text + image) for enhanced retrieval and description.",
        "Offers high accuracy in understanding both textual and visual context.",
        "Cloud-hosted for scalability and easy deployment.",
      ],
    },
    {
      component: "Framework",
      technology: "FastAPI (Backend)",
      reason: [
        "Lightweight, high-performance web framework for APIs.",
        "Asynchronous support ensures fast request handling.",
        "Easy integration with ML models and vector databases.",
      ],
    },
    {
      component: "Vector Database",
      technology: "ChromaDB",
      reason: [
        "Optimized for embeddings storage and retrieval.",
        "Supports fast and efficient similarity search.",
        "Easy to integrate with FastAPI and LLMs.",
      ],
    },
    {
      component: "Relevance Ranking",
      technology: "Cosine Similarity",
      reason: [
        "Measures text-image embedding similarity efficiently.",
        "Computationally lightweight and effective for semantic search.",
        "Works well with ChromaDB for ranking retrieved images.",
      ],
    }, {
      component: "Embedding Model",
      technology: "Contrastive Language-Image Pretraining",
      reason: [
        "Generates shared embeddings for text and image similarity.",
        "Captures deep relationships between text and images.",
        "High accuracy in image retrieval with query in both modlities.",
      ],
    },
  ];



  return (
    <div className="bg-gray-800 h-auto min-h-screen">
        < NavBar />
        <div className="pt-[90px] py-10 flex flex-col items-center justify-center p-5">
            <h1 className="mb-5 font-bold text-white text-4xl">Conversational Memory Bot</h1>
            <h2 className="mb-10 font-bold text-white text-3xl">Your AI-Powered Photo Gallery Assistant</h2>
            <div className="flex flex-col items-center my-10">
                <div className="flex gap-4 mb-10 mx-10">
                    <p className=" text-lg text-white text-justify">
                        The Conversational Memory Bot is an innovative AI-powered assistant designed to transform how users
                        interact
                        with their personal photo galleries. By leveraging advanced natural language processing and visual
                        recognition technologies, the bot allows users to search, explore, and organize their photos using
                        simple,
                        everyday language. For example, users can ask questions like, "Show me photos of my dog playing in
                        the
                        park," or "Find pictures from my trip to Italy in 2021," and the bot will retrieve the relevant
                        images based
                        on the context and content of the photos.
                    </p>
                    <img src={Chatbot} alt="chatbot/home image"
                         className="shadow-sm shadow-green-500 w-auto h-[300px]"
                    />
                </div>
                <div className="w-[80%] my-4">
                    <div className="mx-auto">
                        <p className="text-white text-2xl font-semibold text-center mb-5">Tech-stack chosen and why?</p>
                        <table className="text-white min-w-full border border-gray-300 shadow-md">
                            <thead>
                            <tr className="text-xl bg-gray-800 text-white">
                                <th className="px-4 py-2 text-center">Component</th>
                                <th className="px-4 py-2 text-center">Chosen Technology</th>
                                <th className="px-4 py-2 text-center">Reason for Choice</th>
                            </tr>
                            </thead>
                            <tbody>
                            {data.map((item, index) => (
                                <tr key={index} className="text-lg border-b hover:bg-gray-700">
                                    <td className="px-4 py-2 font-medium">{item.component}</td>
                                    <td className="px-4 py-2">{item.technology}</td>
                                    <td className="px-4 py-2">
                                        <ul className="list-disc ml-4">
                                            {item.reason.map((reason, i) => (
                                                <li key={i}>{reason}</li>
                                            ))}
                                        </ul>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="flex flex-col py-5 mx-10">
                <div className="w-[100%] mb-10 flex pb-8 gap-8">
                    <div>
                        <p className="text-white text-2xl font-semibold mb-2">What this system do?</p>
                        <ul className="text-lg text-white flex flex-col mb-2">
                            {what.map(item => (
                                <li key={item.id}>{item.text}</li>
                            ))}
                        </ul>
                    </div>
                    <img src={Imageuploader} alt="chatbot/home image"
                         className="shadow shadow-amber-200 w-auto h-[300px]"
                    />
                </div>
                <div className="w-[100%] mb-10 text-white flex pb-8 gap-8">
                    <img src={Gallery} alt="chatbot/home image"
                         className="shadow shadow-amber-200 w-auto h-[300px]"
                    />
                    <div>
                        <p className="text-2xl font-semibold mb-2">Why this system?</p>
                        <ul className="flex flex-col text-lg">
                            {why.map(item => (
                                <li key={item.id}>{item.text}</li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="w-[100%] text-white flex gap-8">
                    <div>
                        <p className="text-2xl font-semibold mb-2">How to Use?</p>
                        <ul className="flex flex-col text-lg">
                            {how.map(item => (
                                <li key={item.id}>{item.text}</li>
                            ))}
                        </ul>
                    </div>
                    <img src={Imageviewer} alt="chatbot/home image"
                         className="shadow shadow-amber-200 w-auto h-[300px]"
                    />
                </div>
            </div>
        </div>
    </div>
  );
}

export default HomePage;