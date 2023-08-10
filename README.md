# HLS Status Page

Webpage to display metrics from the cloud processing and provide status based on the metrics.

## Technical Stack

- **Front End:** React JS Framework
- **Back End:** AWS Lambda / AWS Cloudwatch
- **REST API Layer:** AWS Lambda

## Rest API Endpoints
### GET /alarms/

Get the alarms status for the following alarms:
- L30
  - Produced Granules w/in Expected Range
  - Atmospheric Parameters Received
  - Nominal % Processing Errors

- S30
  - Produced Granules w/in Expected Range
  - Atmospheric Parameters Received
  - Nominal % Processing Errors

**Example Request**
```bash
curl '/alarms/'
```

**Example Response**
```json
{
"statusCode": 200,
"body": "[{\"alarms\": {\"Produced Granules w/in Expected Range\": {\"state\": \"OK\", \"state_transitioned_timestamp\": \"2023-08-09 00:40:58.495000+00:00\", \"state_updated_timestamp\": \"2023-08-09 00:40:58.495000+00:00\"}, \"Atmospheric Parameters Received\": {\"state\": \"OK\", \"state_transitioned_timestamp\": \"2023-08-10 05:23:30.604000+00:00\", \"state_updated_timestamp\": \"2023-08-10 05:23:30.604000+00:00\"}, \"Nominal % Processing Errors\": {\"state\": \"OK\", \"state_transitioned_timestamp\": \"2023-08-10 06:39:37.381000+00:00\", \"state_updated_timestamp\": \"2023-08-10 06:39:37.381000+00:00\"}}, \"status\": \"OK\", \"alarm_name\": \"L30 Status\", \"state_updated_timestamp\": \"2023-08-09 00:40:58.495000+00:00\"}, {\"alarms\": {\"Produced Granules w/in Expected Range\": {\"state\": \"ALARM\", \"state_transitioned_timestamp\": \"2023-08-10 07:09:20.862000+00:00\", \"state_updated_timestamp\": \"2023-08-10 07:09:20.862000+00:00\"}, \"Atmospheric Parameters Received\": {\"state\": \"OK\", \"state_transitioned_timestamp\": \"2023-08-10 05:23:30.604000+00:00\", \"state_updated_timestamp\": \"2023-08-10 05:23:30.604000+00:00\"}, \"Nominal % Processing Errors\": {\"state\": \"INSUFFICIENT_DATA\", \"state_transitioned_timestamp\": \"2023-08-10 11:50:57.804000+00:00\", \"state_updated_timestamp\": \"2023-08-10 11:50:57.804000+00:00\"}}, \"status\": \"DANGER\", \"alarm_name\": \"S30 Status\", \"state_updated_timestamp\": \"2023-08-10 07:09:20.862000+00:00\"}]"
}
```

### GET /metrics/?metric=l30&period=24

Retrieve metric data about granules produced for the following alarms:

- **L30**
  - ExecutionsSucceeded
  - Started
  - Succeeded
  - Failed
  - TimedOut
  - Throttled
  - Aborted
- **S30**
  - ExecutionsSucceeded
  - Started
  - Succeeded
  - Failed
  - TimedOut
  - Throttled
  - Aborted

**Example Request:**
```bash
curl 'https://6af2xo7p46.execute-api.us-east-2.amazonaws.com/dev/metrics/?metric=l30&period=24'
```

**Parameters:**

- **metric**: The name for the alarm whose metric data is to be pulled. Accepted values are ‘l30’ and ‘s30’. Default metric value in case of no metric name provided or invalid metric name provided is ‘l30’.
  
- **period**: The number in hours for the range of data. Accepted values are 1(1 hour), 3(3 hours), 12(12 hours), 24(1 day), 72(3 days), 168(1 week). Default period value in case of no period value provided or invalid period value provided is 24.

**Example Response**
```json
{
"statusCode": 200,
"body": "{\"MetricDataResults\": [{\"Id\": \"m1\", \"Label\": \"ExecutionsSucceeded\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [4589.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m2\", \"Label\": \"Started\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [1907.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m3\", \"Label\": \"Succeeded\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [4589.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m4\", \"Label\": \"Failed\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [49.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m5\", \"Label\": \"TimedOut\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [0.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m6\", \"Label\": \"Throttled\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [0.0], \"StatusCode\": \"Complete\"}, {\"Id\": \"m7\", \"Label\": \"Aborted\", \"Timestamps\": [\"2023-08-09 00:00:00+00:00\"], \"Values\": [0.0], \"StatusCode\": \"Complete\"}], \"Messages\": [], \"ResponseMetadata\": {\"RequestId\": \"33351834-e202-4fdf-8076-2279366d3e71\", \"HTTPStatusCode\": 200, \"HTTPHeaders\": {\"x-amzn-requestid\": \"33351834-e202-4fdf-8076-2279366d3e71\", \"content-type\": \"text/xml\", \"content-length\": \"2319\", \"date\": \"Thu, 10 Aug 2023 16:36:23 GMT\"}, \"RetryAttempts\": 0}}"
}

```

### GET /rss/

Retrieve the RSS feed from the United States Geological Survey website.

**Example Request:**
```bash
curl  'https://6af2xo7p46.execute-api.us-east-2.amazonaws.com/dev/rss/'
```

**Example Response**
```json
{
"statusCode": 200,
"headers": {
"Content-Type": "application/xml",
"Access-Control-Allow-Origin": "*"
},
"body": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rss version=\"2.0\" xml:base=\"https://www.usgs.gov/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" xmlns:foaf=\"http://xmlns.com/foaf/0.1/\" xmlns:og=\"http://ogp.me/ns#\" xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" xmlns:schema=\"http://schema.org/\" xmlns:sioc=\"http://rdfs.org/sioc/ns#\" xmlns:sioct=\"http://rdfs.org/sioc/types#\" xmlns:skos=\"http://www.w3.org/2004/02/skos/core#\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\" xmlns:atom=\"http://www.w3.org/2005/Atom\">\n <channel>\n <title>Landsat Missions</title>\n <description>RSS feed of news related to Landsat Missions</description>\n <link>https://www.usgs.gov/</link>\n <atom:link href=\"https://www.usgs.gov/science-support/322/news/feed\" rel=\"self\" type=\"application/rss+xml\" />\n <language>en</language>\n \n <item>\n<title>Current Landsat Science Team Reflects at Final Meeting</title>\n <link>https://www.usgs.gov/landsat-missions/news/current-landsat-science-team-reflects-final-meeting?utm_source=comms&amp;amp;utm_medium=rss&amp;amp;utm_campaign=news</link>\n <description>&lt;p&gt;The Winter 2023 USGS-NASA Landsat Science Team (LST) meeting was held February 7-9, 2023, at the Desert Research Institute in Reno, Nevada. This meeting concludes the five-year term of the current team. &lt;/p&gt;</description>\n <pubDate>Thu, 2 Mar 2023 15:25:54 EST\n</pubDate>\n <dc:creator>lowen@contractor.usgs.gov</dc:creator>\n <guid isPermaLink=\"false\">f0d4f95c-c6ec-45b7-91ed-b1e2dca796ff</guid>\n <author>lowen@contractor.usgs.gov (lowen@contractor.usgs.gov)</author>\n <source url=\"https://www.usgs.gov/science-support/322/news/feed\">U.S. Geological Survey</source>\n</item>\n\n </channel>\n</rss>\n"
}

```
## Errors

| **Status Codes** | **Status Meanings** |
|----------------|-------------------|
| 200 - OK | Successful request and response. |
| 404 - Not Found | The requested resource doesn't exist. |
| 500 - Server Error | Something went wrong on the HLS server end. |

# React Frontend
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Basic Commands

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

