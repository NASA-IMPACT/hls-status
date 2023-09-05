import json
import boto3
from datetime import datetime, timedelta
import os

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name=os.getenv("region_name"))
    period = 24
    metric = 's30'
    
    s30_state_machine_arn = os.getenv("s30_state_machine_arn", "")
    l30_state_machine_arn = os.getenv("l30_state_machine_arn", "")
    no_new_laads_alarm_name = 'No new LAADS'
    
    response = cloudwatch.describe_alarms(AlarmNames=[no_new_laads_alarm_name])
    no_new_laads_alarm = response['MetricAlarms'][0]

    metric_data_query = [
        {
            'Id': 'm0',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsSucceeded',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': s30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        },
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsStarted',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': s30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        },
        {
            'Id': 'm2',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsFailed',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': s30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        },
        {
            'Id': 'm3',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsSucceeded',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': l30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        },
        {
            'Id': 'm4',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsStarted',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': l30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        },
        {
            'Id': 'm5',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsFailed',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': l30_state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            }
        }
    ]
    
    
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=period)
    
    
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_query,
        StartTime=start_time,
        EndTime=end_time
    )
    
    s30_granulues_produced = response["MetricDataResults"][0]["Values"][0]
    s30_granulues_produced_timestamp = response["MetricDataResults"][0]["Timestamps"][0]
    s30_granulues_started = response["MetricDataResults"][1]["Values"][0]
    s30_granulues_failed = response["MetricDataResults"][2]["Values"][0]
    l30_granulues_produced = response["MetricDataResults"][3]["Values"][0]
    l30_granulues_produced_timestamp = response["MetricDataResults"][0]["Timestamps"][0]
    l30_granulues_started = response["MetricDataResults"][4]["Values"][0]
    l30_granulues_failed = response["MetricDataResults"][5]["Values"][0]
    
    
    s30_granulues_produced_status = ""
    l30_granulues_produced_status = ""
    s30_nominal_failed_status = ""
    l30_nominal_failed_status = ""
        
    if s30_granulues_produced < 5000:
        print("red")
        s30_granulues_produced_status = "DANGER"
    elif l30_granulues_produced < 7000:
        print("yellow")
        s30_granulues_produced_status = "ALERT"
    else:
        print("green")
        s30_granulues_produced_status = "OK"

    if l30_granulues_produced < 5000:
        print("red")
        l30_granulues_produced_status = "DANGER"
    elif l30_granulues_produced < 7000:
        print("yellow")
        l30_granulues_produced_status = "ALERT"
    else:
        print("green")
        l30_granulues_produced_status = "OK"

    s30_nominal_failed = (s30_granulues_failed/s30_granulues_started)
    
    if s30_nominal_failed > 0.2:
        print("red")
        s30_nominal_failed_status = "DANGER"
    elif s30_nominal_failed > 0.1 and s30_nominal_failed < 0.2:
        print("yellow")
        s30_nominal_failed_status = "ALERT"
    else:
        print("green")
        s30_nominal_failed_status = "OK"
    
    l30_nominal_failed = (l30_granulues_failed/l30_granulues_started)
    
    if l30_nominal_failed > 0.2:
        print("l30 red")
        l30_nominal_failed_status = "DANGER"
    elif l30_nominal_failed > 0.1 and l30_nominal_failed < 0.2:
        print("l30 yellow")
        l30_nominal_failed_status = "ALERT"
    else:
        print("l30 green")
        l30_nominal_failed_status = "OK"
        
    s30_alarms_res = {
        'Produced Granules w/in Expected Range': {
            'state': s30_granulues_produced_status,
            'state_transitioned_timestamp': s30_granulues_produced_timestamp,
            'state_updated_timestamp': s30_granulues_produced_timestamp,
        },
        'Atmospheric Parameters Received': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Nominal % Processing Errors': {
            'state': s30_nominal_failed_status,
            'state_transitioned_timestamp': s30_granulues_produced_timestamp,
            'state_updated_timestamp': s30_granulues_produced_timestamp
        }
    }
    
    l30_alarms_res = {
        'Produced Granules w/in Expected Range': {
            'state': l30_granulues_produced_status,
            'state_transitioned_timestamp': s30_granulues_produced_timestamp,
            'state_updated_timestamp': s30_granulues_produced_timestamp,
        },
        'Atmospheric Parameters Received': {
            'state': no_new_laads_alarm['StateValue'],
            'state_transitioned_timestamp': no_new_laads_alarm['StateTransitionedTimestamp'],
            'state_updated_timestamp': no_new_laads_alarm['StateUpdatedTimestamp']
        },
        'Nominal % Processing Errors': {
            'state': s30_nominal_failed_status,
            'state_transitioned_timestamp': s30_granulues_produced_timestamp,
            'state_updated_timestamp': s30_granulues_produced_timestamp
        }
    }
    
    if (
        s30_nominal_failed_status == 'OK' and
        no_new_laads_alarm['StateValue'] == 'OK'
        ):
            if s30_granulues_produced_status == 'OK':
                s30_status = "OK"
            else:
                s30_status = 'ALERT'
    else:
        s30_status = 'DANGER'

    if (
        l30_nominal_failed_status == 'OK' and
        no_new_laads_alarm['StateValue'] == 'OK'
        ):
            if l30_granulues_produced_status == 'OK':
                l30_status = "OK"
            else:
                l30_status = 'ALERT'
    else:
        l30_status = 'DANGER'
    
    alarms_res = []
    alarms_res.append(
        {'alarms': l30_alarms_res, 'status': l30_status, 'alarm_name': 'L30 Status', 'state_updated_timestamp': l30_granulues_produced_timestamp},
    )
    
    alarms_res.append(
        {'alarms': s30_alarms_res, 'status': s30_status, 'alarm_name': 'S30 Status', 'state_updated_timestamp': s30_granulues_produced_timestamp}
    )
    return {
        'statusCode': 200,
        'body': json.dumps(alarms_res, default=str)
    }