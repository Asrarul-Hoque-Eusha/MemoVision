import { Link } from 'react-router-dom';

const Navbar = () => {

  const navItems = [
    { id: 1, text: 'Home', link: '/' },
    { id: 2, text: 'Gallery', link: '/gallery' },
    { id: 3, text: 'Image Uploader', link: '/upload' },
    { id: 5, text: 'Chat', link: '/chat' },
  ];

  return (

    <div className='fixed top-0 w-screen bg-gray-500 '>
      <div className='flex justify-between items-center h-[80px] max-w-[1240px] mx-auto px-4 text-black'>
        <h1 className='w-full text-3xl font-bold text-white'>MemoVision</h1>

        <ul className='flex text-center'>
          {navItems.map(item => (
              <Link key={item.id} to={item.link} >
                <li
                  //key={item.id}
                  className='px-1 py-3 text-white font-bold w-[130px] hover:bg-[#9df7da] rounded-xl m-2
                  cursor-pointer duration-300 hover:text-black'
                >
                  {item.text}
                </li>
              </Link>
          ))}
        </ul>

      </div>
    </div>
  );
};

export default Navbar;