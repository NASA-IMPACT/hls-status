import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { BeatLoader } from 'react-spinners';
import ReactPaginate from 'react-paginate';
import '../styles/RSSFeed.css';
import { INTHUB_RSS_FEED_URL } from '../utilities/config';


function RssFeedPage() {
    const location = useLocation();

    let items = location.state.allItems;

    const [allItems, setAllItems] = useState([]);
    const [rssLoading, setRSSLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(0);
    const itemsPerPage = 10; // Number of items to display per page
    const pageCount = Math.ceil(allItems.length / itemsPerPage); // Calculate the total number of pages


    useEffect(() => {
        setRSSLoading(true);
        if (items) {

            setRSSLoading(false);
            setAllItems(items);
        }
        else {

            fetch(INTHUB_RSS_FEED_URL)
                .then(response => response.text())
                .then(data => {

                    const parser = new DOMParser();
                    const xml = parser.parseFromString(data, 'application/xml');

                    const allItems = Array.from(xml.querySelectorAll('item')).map(item => ({
                        title: item.querySelector('title').textContent,
                        link: item.querySelector('link').textContent,
                        description: item.querySelector('description').textContent,
                        pubDate: item.querySelector('pubDate').textContent,
                        guid: item.querySelector('guid').textContent,
                    }));
                    setRSSLoading(false);
                    setAllItems(allItems);


                })
                .catch(error => {
                    console.log(error);
                });
        }

    }, []);

    const handlePageChange = (selectedPage) => {
        setCurrentPage(selectedPage.selected);
    };

    const offset = currentPage * itemsPerPage;
    const paginatedItems = allItems.slice(offset, offset + itemsPerPage).map((item, index) => (
        <div key={index} className="feed-item">
            <h2 className="feed-item-title">{item.title}</h2>
            {/* <p className="feed-item-description">{item.description}</p> */}
            <div className="feed-item-details">
                <p className="feed-item-description">
                    <i className="far fa-calendar-alt calendar-icon"></i>
                    <span className="greyed-out">{item.pubDate}</span>
                </p>
                <a className="feed-item-link" href={item.link} target='_blank' rel="noreferrer">Read More <i className="fas fa-external-link-alt" aria-hidden="true"></i></a>
            </div>
        </div>
    ));


    return (
        <div className="all-rss-container">
            <h1 className="title-content">All News <i className="fa fa-rss"></i></h1>
            {rssLoading ? (
                <BeatLoader color="#36D7B7" loading={rssLoading} />
            ) : (
                <>
                    {paginatedItems}
                    <ReactPaginate
                        previousLabel={'Previous'}
                        nextLabel={'Next'}
                        pageCount={pageCount}
                        onPageChange={handlePageChange}
                        containerClassName={"pagination"}
                        previousLinkClassName={"pagination__link"}
                        nextLinkClassName={"pagination__link"}
                        disabledClassName={"pagination__link--disabled"}
                        activeClassName={"pagination__link--active"}
                    />

                </>
            )}
        </div>

    );
}


export default RssFeedPage;
