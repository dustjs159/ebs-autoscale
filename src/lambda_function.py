import time
import logging
import json
from ec2 import describe_instance
from ec2 import describe_volumes
from ec2 import modify_volume
from ssm import run_command
from ssm import command_status_check
from sns import sns_publish
    
def lambda_handler(event, context):
    
    logger = logging.getLogger(context.aws_request_id)
    logger.setLevel(logging.DEBUG)
    
    payload = json.loads(event["Records"][0]["Sns"]["Message"])
    
    try:
        instance_info = payload["Trigger"]["Dimensions"][1]["name"]
        if instance_info == "InstanceId":
            logger.info("Trigger contain instance id")
            instance_id = payload["Trigger"]["Dimensions"][1]["value"]
            logger.info(f"Instance ID : {instance_id}")
            volume_id, original_volume_size = describe_volumes(instance_id)
            logger.info(f"Volume ID : {volume_id}, original_volume_size : {original_volume_size}")
            resized_volume_size, status_code = modify_volume(volume_id, original_volume_size)
            logger.info(f"resized_volume_size : {resized_volume_size}, status_code : {status_code}")
            if status_code == 200:
                logger.info(f"Success Modify EBS Volume. Original Volume Size : {original_volume_size}, Resized Volume Size : {resized_volume_size}")
                time.sleep(30)
                command_id = run_command(instance_id)                                                                                                                                                                                                                                                                                                                                                                  
                command_status = command_status_check(instance_id, command_id)
                host = describe_instance(instance_id)
                sns_publish(command_status, host, instance_id, original_volume_size, resized_volume_size)
            else:
                logger.error(f"Failed Modify EBS Volume, Status Code : {status_code}")
        else:
            logger.error("Trigger does not contain instance id")       
    except Exception as e:
        logger.error(e)
