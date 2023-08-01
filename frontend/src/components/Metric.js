import { useEffect, useState } from 'react';
import { BeatLoader } from 'react-spinners';
import { useLocation } from 'react-router-dom';
import { Chart, ArcElement, Legend, Tooltip } from 'chart.js'
import { Doughnut } from 'react-chartjs-2';
import { METRIC_URL } from '../utilities/config';
import formatDate from '../utilities/date';
import '../styles/Metric.css';

Chart.register(ArcElement, Legend, Tooltip);


const Metric = (props) => {
    const [metricData, setMetricData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [selectedRange, setSelectedRange] = useState('24');

    const location = useLocation();
    const isFromLink = location.state

    const alarm = isFromLink ? location.state.alarm : props.alarm;
    const isL30Alarm = alarm.alarm_name === 'L30 Status';
    const granulesTitle = isL30Alarm ? 'L30 Granules Produced' : 'S30 Granules Produced';
    const chartTitle = isL30Alarm ? 'L30 Status' : 'S30 Status';

    const labelColors = {
        Succeeded: '#2ca02c',
        Failed: '#d62728',
        TimedOut: '#ff7f0e',
        Throttled: '#dbdb8d',
        Aborted: '#c7c7c7',
    };

    const donutChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'rectRounded'
                },
            },
        },
    };

    const handleTimeRangeSelection = (range) => {
        setSelectedRange(range);
    };

    useEffect(() => {
        const url = isL30Alarm
            ? `${METRIC_URL}?metric=l30&period=${selectedRange}`
            : `${METRIC_URL}?metric=s30&period=${selectedRange}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                setLoading(false);
                let content = JSON.parse(data.body);
                setMetricData(content.MetricDataResults);
            })
            .catch(error => {
                setError(true);
                console.error(error);
            });
    }, [selectedRange]);

    const executionsSucceededData = metricData.filter(metric => metric.Label === 'ExecutionsSucceeded');
    const otherData = metricData.filter(metric => metric.Label !== 'ExecutionsSucceeded');

    const labels = otherData.map((metric) => metric.Label);
    const values = otherData.map((metric) => metric.Values && metric.Values.length > 0 ? metric.Values[0] : 0);

    const chartData = {
        labels: labels,
        datasets: [
            {
                data: values,
                backgroundColor: labels.map((label) => labelColors[label] || '#1f77b4'),
            },
        ],
    };

    return (
        <div className={`${isFromLink ? 'widget' : 'widget-min'}`}>
            {loading ? (
                <div className="loader-container">
                    <BeatLoader color="#36D7B7" loading={loading} />
                </div>
            ) : error ? (
                <div className="no-data-message">No data available</div>
            ) : (
                <div>
                    {isFromLink && (
                        <div className="time-range-buttons">
                            <button
                                className={selectedRange === '1' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('1')}
                            >
                                1h
                            </button>
                            <button
                                className={selectedRange === '3' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('3')}
                            >
                                3h
                            </button>
                            <button
                                className={selectedRange === '12' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('12')}
                            >
                                12h
                            </button>
                            <button
                                className={selectedRange === '24' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('24')}
                            >
                                1d
                            </button>
                            <button
                                className={selectedRange === '72' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('72')}
                            >
                                3d
                            </button>
                            <button
                                className={selectedRange === '168' ? 'active' : ''}
                                onClick={() => handleTimeRangeSelection('168')}
                            >
                                1w
                            </button>
                        </div>)}
                    <div className="horizontal-container">
                        {executionsSucceededData.map((data, index) => (
                            <div key={index} className="metric-widget">
                                <div className="widget-item">
                                    <h4 className="widget-value">{granulesTitle}</h4>
                                </div>

                                <div className="widget-item center-value">
                                    <h2 className="widget-value large-value">{data.Values[0] ? data.Values[0].toLocaleString() : "--"}</h2>
                                </div>
                                <div className="widget-item center-value">
                                    <span className="widget-value">{data.Timestamps[0] ? formatDate(data.Timestamps[0]) : "--"}</span>
                                </div>
                            </div>
                        ))}
                        <div className="metric-widget">
                            <h3>{chartTitle}</h3>
                            <div className="chart-container">
                                <Doughnut data={chartData} options={donutChartOptions} />
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Metric;
