import json
import boto3
from datetime import datetime, timedelta
import os

def granules_status_determination(value, thresholds):
    if value < thresholds[0]:
        return ('DANGER', f'Granules Succeeded is less than {thresholds[0]}')
    elif value < thresholds[1]:
        return ('ALERT', f'Granules Succeeded is less than {thresholds[1]}')
    else:
        return ('OK', 'OK')
        
def error_status_determination(value, thresholds):
    if value > thresholds[0]:
        return ('DANGER',f'More than {thresholds[0] * 100}% Granules Failed in the past 24 hours')
    elif value > thresholds[1]:
        return ('ALERT', f'More than {thresholds[1] * 100}% Granules Failed in the past 24 hours')
    else:
        return ('OK', 'OK')
        
def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name=os.getenv('region_name'))
    period = 24
    
    s30_state_machine_arn = os.getenv("s30_state_machine_arn", "")
    l30_state_machine_arn = os.getenv("l30_state_machine_arn", "")
    no_new_laads_alarm_name = os.getenv("no_new_laads_alarm_name", "")
    
    metric_data_query = []
    for metric_name, arn in [('ExecutionsSucceeded', s30_state_machine_arn),
                             ('ExecutionsStarted', s30_state_machine_arn),
                             ('ExecutionsFailed', s30_state_machine_arn),
                             ('ExecutionsSucceeded', l30_state_machine_arn),
                             ('ExecutionsStarted', l30_state_machine_arn),
                             ('ExecutionsFailed', l30_state_machine_arn)]:
        metric_data_query.append({
            'Id': 'm'+str(len(metric_data_query)),
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': metric_name,
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        })
        
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=period)
    # end_time = datetime.now()
    end_time_midnight = end_time.replace(hour=0, minute=0, second=0)
    start_time = end_time_midnight - timedelta(hours=period)
        
    no_new_laads_alarm_response = cloudwatch.describe_alarms(AlarmNames=[no_new_laads_alarm_name])
    no_new_laads_alarm = no_new_laads_alarm_response['MetricAlarms'][0]
    
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_query,
        StartTime=start_time,
        EndTime=end_time
    )

    metric_results = response["MetricDataResults"]    
    
    s30_granulues_produced_status, s30_granulues_produced_info  = granules_status_determination(metric_results[0]["Values"][0], [5000, 7000])
    l30_granulues_produced_status, l30_granulues_produced_info = granules_status_determination(metric_results[3]["Values"][0], [5000, 7000])
    
    s30_nominal_failed_status, s30_nominal_failed_info = error_status_determination(metric_results[2]["Values"][0] / metric_results[1]["Values"][0], [0.2, 0.1])
    l30_nominal_failed_status, l30_nominal_failed_info = error_status_determination(metric_results[5]["Values"][0] / metric_results[4]["Values"][0], [0.2, 0.1])
    
    no_new_laads_alarm_status = 'DANGER' if no_new_laads_alarm['StateValue'] == 'ALARM' else 'ALERT' if no_new_laads_alarm['StateValue'] == 'Insufficient data' else no_new_laads_alarm['StateValue'] 

    no_new_laads_alarm_info = {
        'Atmospheric Parameters Received': {
            'state': no_new_laads_alarm_status,
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        }
    }
        
    s30_alarms_res = {
        **no_new_laads_alarm_info,
        'Produced Granules w/in Expected Range': {
            'state': s30_granulues_produced_status,
            'info': s30_granulues_produced_info,
            'state_transitioned_timestamp': metric_results[0]["Timestamps"][0],
            'state_updated_timestamp': metric_results[0]["Timestamps"][0],
        },
        'Nominal % Processing Errors': {
            'state': s30_nominal_failed_status,
            'info': s30_nominal_failed_info,
            'state_transitioned_timestamp': metric_results[0]["Timestamps"][0],
            'state_updated_timestamp': metric_results[0]["Timestamps"][0]
        }
    }

    l30_alarms_res = {
        **no_new_laads_alarm_info,
        'Produced Granules w/in Expected Range': {
            'state': l30_granulues_produced_status,
            'info': l30_granulues_produced_info,
            'state_transitioned_timestamp': metric_results[3]["Timestamps"][0],
            'state_updated_timestamp': metric_results[3]["Timestamps"][0],
        },
        'Nominal % Processing Errors': {
            'state': l30_nominal_failed_status,
            'info': l30_nominal_failed_info,
            'state_transitioned_timestamp': metric_results[3]["Timestamps"][0],
            'state_updated_timestamp': metric_results[3]["Timestamps"][0]
        }
    }
    
    # s30_status = "DANGER" if s30_granulues_produced_status == "DANGER" or no_new_laads_alarm['StateValue'] == "DANGER" or s30_nominal_failed_status == "DANGER" else s30_granulues_produced_status
    # l30_status = "DANGER" if l30_granulues_produced_status == "DANGER" or no_new_laads_alarm['StateValue'] == "DANGER" or l30_nominal_failed_status == "DANGER" else l30_granulues_produced_status

    if (
        s30_nominal_failed_status == 'DANGER' or
        no_new_laads_alarm['StateValue'] == 'DANGER'
        ):
            s30_status = 'DANGER'
    elif (
        s30_nominal_failed_status == 'ALERT' or
        no_new_laads_alarm['StateValue'] == 'ALERT'
        ):
            s30_status = 'ALERT'
    else:
        s30_status = 'ALERT' if (s30_granulues_produced_status == 'ALERT' or s30_granulues_produced_status == 'DANGER') else 'OK'

    if (
        l30_nominal_failed_status == 'DANGER' or
        no_new_laads_alarm['StateValue'] == 'DANGER'
        ):
            l30_status = 'DANGER'
    elif (
        l30_nominal_failed_status == 'ALERT' or
        no_new_laads_alarm['StateValue'] == 'ALERT'
        ):
            l30_status = 'ALERT'
    else:
        l30_status = 'ALERT' if (l30_granulues_produced_status == 'ALERT' or l30_granulues_produced_status == 'DANGER') else 'OK'
    
    alarms_res = [
        {'alarms': l30_alarms_res, 'status': l30_status, 'alarm_name': 'L30 Status', 'state_updated_timestamp': metric_results[3]["Timestamps"][0]},
        {'alarms': s30_alarms_res, 'status': s30_status, 'alarm_name': 'S30 Status', 'state_updated_timestamp': metric_results[0]["Timestamps"][0]}
    ]
    
    return {
        'status_code': 200,
        'body': json.dumps(alarms_res, default=str)
    }