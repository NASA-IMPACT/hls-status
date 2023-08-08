import json
import boto3
import os

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name=os.getenv('region_name'))
    
    # Initialize alarms
    l30_alarm_name = os.getenv('l30_alarm')
    s30_alarm_name = os.getenv('s30_alarm')
    no_new_laads_alarm_name = os.getenv('no_new_laads_alarm')
    landsat_alarm_name = os.getenv('landsat_alarm')
    sentinel_alarm_name = os.getenv('sentinel_alarm')

    alarm_names = [l30_alarm_name, s30_alarm_name, no_new_laads_alarm_name, landsat_alarm_name, sentinel_alarm_name ]

    response = cloudwatch.describe_alarms(AlarmNames=alarm_names)
    alarms = response['MetricAlarms']

    l30_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == l30_alarm_name), None)
    s30_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == s30_alarm_name), None)
    no_new_laads_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == no_new_laads_alarm_name), None)
    landsat_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == landsat_alarm_name), None)
    sentinel_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == sentinel_alarm_name), None)

    l30_status = "OK"
    s30_status = "OK"
    if (
        l30_alarm and
        no_new_laads_alarm and no_new_laads_alarm['StateValue'] == 'OK' and
        landsat_alarm and landsat_alarm['StateValue'] == 'OK'
    ):
        if l30_alarm['StateValue'] == 'OK':
            l30_status = "OK"
        else:
            l30_status = 'ALERT'
    else:
        l30_status = 'DANGER'
        
    if (
        s30_alarm and
        no_new_laads_alarm and no_new_laads_alarm['StateValue'] == 'OK' and
        sentinel_alarm and sentinel_alarm['StateValue'] == 'OK'
    ):
        if s30_alarm['StateValue'] == 'OK':
            s30_status = 'OK'
        else:
            s30_status = 'ALERT'
    else:
        s30_status = 'DANGER'

    alarms_res = []
    l30_alarms_res = {
        'Produced Granules w/in Expected Ranged': {
            'state': l30_alarm['StateValue'],
            'state_transitioned_timestamp': l30_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': l30_alarm['StateUpdatedTimestamp'],
        },
        'Atmospheric Parameters Received': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Nominal % Processing Errors': {
            'state': landsat_alarm['StateValue'],
            'state_transitioned_timestamp': landsat_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': landsat_alarm['StateUpdatedTimestamp']
        }
    }

    s30_alarms_res = {
        'Produced Granules w/in Expected Ranged': {
            'state': s30_alarm['StateValue'],
            'state_transitioned_timestamp': s30_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': s30_alarm['StateUpdatedTimestamp'],
        },
        'Atmospheric Parameters Received': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Nominal % Processing Errors': {
            'state': sentinel_alarm['StateValue'],
            'state_transitioned_timestamp': sentinel_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': sentinel_alarm['StateUpdatedTimestamp']
        }
    }

    alarms_res.append(
        {'alarms': l30_alarms_res, 'status': l30_status, 'alarm_name': 'L30 Status', 'state_updated_timestamp': l30_alarm['StateTransitionedTimestamp']},
    )
    
    alarms_res.append(
        {'alarms': s30_alarms_res, 'status': s30_status, 'alarm_name': 'S30 Status', 'state_updated_timestamp': s30_alarm['StateTransitionedTimestamp']}
    )
          
    return {
        'statusCode': 200,
        'body': json.dumps(alarms_res, default=str)
    }