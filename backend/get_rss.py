import urllib.request

def lambda_handler(event, context):
    # Retrieve the RSS feed URL from the event
    # rss_feed_url = event['rss_feed_url']
    
    # Fetch the XML RSS feed
    try:
        response = urllib.request.urlopen('https://www.usgs.gov/science-support/322/news/feed')
        rss_xml = response.read().decode('utf-8')
        rss_xml = rss_xml.lstrip('\ufeff')
        
        # Set the appropriate response headers
        headers = {
            'Content-Type': 'application/xml',
            'Access-Control-Allow-Origin': '*'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': rss_xml
        }
    except Exception as e:
        # Handle any errors that occur during the fetching process
        return {
            'statusCode': 500,
            'body': str(e)
        }