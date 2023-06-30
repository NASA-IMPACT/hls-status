import React, { useState, useEffect } from 'react';
import '../styles/StylePage.css';
import { BeatLoader } from 'react-spinners';
import { Link } from 'react-router-dom';
import Metric from '../components/Metric';
import { ALARM_URL, INTHUB_RSS_FEED_URL, USGS_RSS_FEED_URL, HLS_TITLE } from '../utilities/config';


function StatusPage() {
  const [alarms, setAlarms] = useState([]);
  const [selectedAlarm, setSelectedAlarm] = useState(null);
  const [feedItems, setFeedItems] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rssLoading, setRSSLoading] = useState(true);

  useEffect(() => {

    setLoading(true);
    setRSSLoading(true);

    const fetchAlarm = () => {
      fetch(ALARM_URL)
        .then(response => response.json())
        .then(data => {
          let content = JSON.parse(data.body);
          setAlarms(content);
        })
        .catch(error => console.error(error))
        .finally(() => setLoading(false));
    };

    const fetchRssFeeds = async () => {
      try {
        const [inthubResponse, usgsResponse] = await Promise.all([
          fetch(INTHUB_RSS_FEED_URL),
          fetch(USGS_RSS_FEED_URL)
        ]);

        const [inthubXml, usgsXml] = await Promise.all([
          inthubResponse.text(),
          usgsResponse.text()
        ]);

        const inthubAllItems = parseXml(inthubXml, true);
        let contentBody = JSON.parse(usgsXml).body;
        const usgsAllItems = parseXml(contentBody, false);

        const mergedItems = [...inthubAllItems, ...usgsAllItems];
        const sortedItems = mergedItems.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
        setFeedItems(sortedItems.slice(0, 5));
        setAllItems(sortedItems);
      }
      catch (error) {
        console.log(error);
      }
      finally {
        setRSSLoading(false);
      }
    };

    Promise.all([fetchRssFeeds(), fetchAlarm()]);
  }, []);

  const parseXml = (response, filter = false) => {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(response, 'application/xml');
    let items = Array.from(xmlDoc.querySelectorAll('item'));
    const excludedRegex = /Sentinel-3[a-zA-Z]?|Sentinel-1[a-zA-Z]?/;
    const filteredItems = items.filter(item => {
      const title = item.querySelector('title').textContent;
      const shouldFilter = !excludedRegex.test(title);
      return filter ? shouldFilter : true;
    });
  
    return filteredItems.map(item => ({
      title: item.querySelector('title').textContent,
      link: item.querySelector('link').textContent,
      description: item.querySelector('description').textContent,
      pubDate: item.querySelector('pubDate').textContent,
      guid: item.querySelector('guid').textContent,
    }));
  }

  const formatDate = timestamp => {
    const date = new Date(timestamp);
    const options = { timeZone: 'UTC', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    const formattedDate = date.toLocaleString('en-US', options);
    const timezone = 'UTC'; // Specify the timezone here

    return `${formattedDate} (${timezone})`;
  };

  const handleAlarmClick = alarm => {
    if (selectedAlarm === alarm) {
      setSelectedAlarm(null); // deselect the alarm if already selected
    } else {
      setSelectedAlarm(alarm); // select the clicked alarm
    }
  };


  return (
    <div>
      <div className="welcome-container">
        <h1 className="welcome-content">Welcome to {HLS_TITLE} Status Page</h1>
      </div>

      <div className="main-container">
        <div className="title-container">
          <h1 className="title-content">HLS Status Past 24 hours</h1>
          {loading ? (
            <div className="loader-container">
              <BeatLoader color="#36D7B7" loading={loading} />
            </div>
          ) : (
            <div>
              {alarms.map((alarm, index) => (
                <div key={index} className={`status-main ${alarm.state === 'OK' ? 'ok-status' : 'danger-status'}`}>
                  <div className="status-container" key={index}>
                    <div className="status-item" >
                      <h3 className="status-title">
                        {alarm.alarm_name}
                      </h3>
                      <div className="status-info">
                        <div className="updated-timestamp">Last Updated on {formatDate(alarm.state_updated_timestamp)}</div>
                      </div>
                    </div>
                    <div className="status-icon">
                      {alarm.state === 'OK' ? (
                        <i className="fas fa-check-circle ok-icon"></i>
                      ) : (
                        <i className="fas fa-exclamation-triangle danger-icon"></i>
                      )}
                    </div>
                  </div>
                  <h4 className="status-header" onClick={() => handleAlarmClick(alarm)}>Details
                    <i style={{ marginLeft: "8px" }} className={selectedAlarm === alarm ? 'fas fa-angle-up' : 'fas fa-angle-down'}></i></h4>
                  {selectedAlarm === alarm && (
                    <div className="status-history">
                      <Metric alarm={alarm} />
                      <h4><Link to='/metrics' state={{ alarm }} className="title-link">View More Details
                        <i style={{ marginLeft: "8px" }} className='fas fa-angle-right'></i></Link></h4>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>


        <div className="rss-container">
          <div className="rss-title-container">
            <h1 className="title-content">Latest News <i className="fa fa-rss"></i></h1>

            <Link to="/all-feeds" className="title-link" state={{ allItems }}>
              <h4>All News</h4>
            </Link>
          </div>
          {rssLoading ? (
            <div className="loader-container">
              <BeatLoader color="#36D7B7" loading={rssLoading} />
            </div>
          ) : (

            <ul style={{ padding: "10px" }}>
              {feedItems.map((item, index) => (
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
              ))}
            </ul>

          )}


        </div>
      </div>
    </div>
  );
}

export default StatusPage;