import React, { useState, useEffect } from 'react';
import '../styles/StylePage.css';
import { BeatLoader } from 'react-spinners';
import { Link } from 'react-router-dom';
import Metric from '../components/Metric';
import {ALARM_URL, RSS_FEED_URL} from '../config';


function StatusPage() {
  const [title, setTitle] = useState("");
  const [alarms, setAlarms] = useState([]);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedAlarm, setSelectedAlarm] = useState(null);
  const [feedItems, setFeedItems] = useState([]);
  const [allItems, setAllItems] = useState([]);
  // const RSS_FEED_URL = 'https://www.usgs.gov/science-support/322/news/feed';
  const [loading, setLoading] = useState(true);
  const [rssLoading, setRSSLoading] = useState(true);

  let alarm = [
    {
      "alarm_name": "L30 Produced 24 hours",
      "state": "OK",
      "state_transitioned_timestamp": "2023-03-07 17:47:34.524000+00:00",
      "state_updated_timestamp": "2023-03-07 17:47:34.524000+00:00",
      "alarm_history_items": []
    },
    {
      "alarm_name": "S30 Produced 24 hours",
      "state": "OK",
      "state_transitioned_timestamp": "2023-04-14 02:38:25.405000+00:00",
      "state_updated_timestamp": "2023-04-14 02:38:25.405000+00:00",
      "alarm_history_items": {
        "version": "1.0",
        "oldState": {
          "stateValue": "ALARM",
          "stateReason": "Threshold Crossed: 1 out of the last 1 datapoints [6986.0 (10/04/23 07:24:00)] was less than the threshold (7000.0) (minimum 1 datapoint for OK -> ALARM transition).",
          "stateReasonData": {
            "version": "1.0",
            "queryDate": "2023-04-11T07:24:25.428+0000",
            "startDate": "2023-04-10T07:24:00.000+0000",
            "statistic": "Sum",
            "period": 86400,
            "recentDatapoints": [
              6986.0
            ],
            "threshold": 7000.0,
            "evaluatedDatapoints": [
              {
                "timestamp": "2023-04-10T07:24:00.000+0000",
                "sampleCount": 18777.0,
                "value": 6986.0
              }
            ]
          }
        },
        "newState": {
          "stateValue": "OK",
          "stateReason": "Threshold Crossed: 1 out of the last 1 datapoints [7007.0 (10/04/23 14:42:00)] was not less than the threshold (7000.0) (minimum 1 datapoint for ALARM -> OK transition).",
          "stateReasonData": {
            "version": "1.0",
            "queryDate": "2023-04-11T14:42:25.397+0000",
            "startDate": "2023-04-10T14:42:00.000+0000",
            "statistic": "Sum",
            "period": 86400,
            "recentDatapoints": [
              7007.0
            ],
            "threshold": 7000.0,
            "evaluatedDatapoints": [
              {
                "timestamp": "2023-04-10T14:42:00.000+0000",
                "sampleCount": 16412.0,
                "value": 7007.0
              }
            ]
          }
        }
      }
    }
  ]

  useEffect(() => {

    setLoading(true);
    setRSSLoading(true);
    fetch(ALARM_URL)
      .then(response => response.json())
      .then(data => {
        setLoading(false);
        let content = JSON.parse(data.body);
        setAlarms(content);
      })
      .catch(error => console.error(error));


    fetch(RSS_FEED_URL)
      .then(response => response.text())
      .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 'application/xml');
        let items = Array.from(xml.querySelectorAll('item'));

        const allItems = items.map(item => ({
          title: item.querySelector('title').textContent,
          link: item.querySelector('link').textContent,
          description: item.querySelector('description').textContent,
          pubDate: item.querySelector('pubDate').textContent,
          guid: item.querySelector('guid').textContent,
        }));
        setRSSLoading(false);
        setFeedItems(allItems.slice(0, 5));
        setAllItems(allItems);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  const formatDate = timestamp => {
    const date = new Date(timestamp);
    const options = { timeZone: 'UTC', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    const formattedDate = date.toLocaleString('en-US', options);
    const timezone = 'UTC'; // Specify the timezone here

    return `${formattedDate} (${timezone})`;
  };

  const toggleDetails = (index) => {
    setSelectedAlarm(alarms[index].alarm_history_items);
    // console.log(selectedAlarm);
    setShowDetails(!showDetails);
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
        <h1 className="welcome-content">Welcome to Harmonized Landsat Sentinel-2 Status Page</h1>
      </div>

      <div style={{ display: "flex", justifyContent: 'center' }}>

        <div className="title-container">
          <h1 className="title-content">HLS Status Past 24 hours</h1>
          {loading ? (
            <BeatLoader color="#36D7B7" loading={loading} />
          ) : (
            <div>
              {alarms.map((alarm, index) => (
                <div className={`status-main ${alarm.state === 'OK' ? 'ok-status' : 'danger-status'}`}>
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
                      <Metric alarm={alarm}/>
                      <h4><Link to='/metrics' state = {{alarm}} className="title-link">View More Details
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
            <BeatLoader color="#36D7B7" loading={rssLoading} />
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
                    <a className="feed-item-link" href={item.link} target='_blank'>Read More <i className="fas fa-external-link-alt" aria-hidden="true"></i></a>
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