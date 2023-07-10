import json
import boto3

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')
    alarm_names = ['S30 Produced 24 hours',
                'L30 Produced 24 hours',
                'hls-production-v2-LandsatStepFunctionAlarmLandsatCWStepFunctionAlarm277F1921-IR80N4G3HDG2',
                'hls-production-v2-SentinelStepFunctionAlarmSentinelCWStepFunctionAlarmBA29C2FB-1FMHFYYGWD7MX',
                'No new LAADS']
    response = cloudwatch.describe_alarms(AlarmNames=alarm_names)
    alarms = response['MetricAlarms']
    

    l30_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == 'L30 Produced 24 hours'), None)
    s30_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == 'S30 Produced 24 hours'), None)
    no_new_laads_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == 'No new LAADS'), None)
    landsat_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == 'hls-production-v2-LandsatStepFunctionAlarmLandsatCWStepFunctionAlarm277F1921-IR80N4G3HDG2'), None)
    sentinel_alarm = next((alarm for alarm in alarms if alarm['AlarmName'] == 'hls-production-v2-SentinelStepFunctionAlarmSentinelCWStepFunctionAlarmBA29C2FB-1FMHFYYGWD7MX'), None)

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
        'L30 Produced 24 hours': {
            'state': l30_alarm['StateValue'],
            'state_transitioned_timestamp': l30_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': l30_alarm['StateUpdatedTimestamp'],
        },
        'No new LAADS': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Landsat': {
            'state': landsat_alarm['StateValue'],
            'state_transitioned_timestamp': landsat_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': landsat_alarm['StateUpdatedTimestamp']
        }
    }

    s30_alarms_res = {
        'S30 Produced 24 hours': {
            'state': s30_alarm['StateValue'],
            'state_transitioned_timestamp': s30_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': s30_alarm['StateUpdatedTimestamp'],
        },
        'No new LAADS': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Sentinel': {
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