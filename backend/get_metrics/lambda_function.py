import json
import boto3
from datetime import datetime, timedelta
import os

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name=os.getenv("region_name"))
    
    period = int(event['period']) if event['period'] else 24
    metric = event['metric'] if event['metric'] else 'l30'
    # period = 24
    # metric = 's30'
    
    state_machine_arn = os.getenv("s30_state_machine_arn", "") if metric == 's30' else os.getenv("l30_state_machine_arn", "")

    metric_data_query = [
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsSucceeded',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
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
                    'MetricName': 'ExecutionsStarted',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
            'Label': 'Started',
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
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
             'Label': 'Succeeded',
        },
        {
            'Id': 'm4',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsFailed',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
             'Label': 'Failed',
        },
        {
            'Id': 'm5',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsTimedOut',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
             'Label': 'TimedOut',
        },
        {
            'Id': 'm6',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionThrottled',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
             'Label': 'Throttled',
        },
         {
            'Id': 'm7',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/States',
                    'MetricName': 'ExecutionsAborted',
                    'Dimensions': [
                        {
                            'Name': 'StateMachineArn',
                            'Value': state_machine_arn
                        }
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum'
            },
             'Label': 'Aborted',
        },
               
    ]

    end_time = datetime.now()
    end_time_midnight = end_time.replace(hour=0, minute=0, second=0)
    start_time = end_time_midnight - timedelta(hours=period)
    
    
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_query,
        StartTime=start_time,
        EndTime=end_time
    )

    
    return {
        'statusCode': 200,
        'body': json.dumps(response, default=str)
    }