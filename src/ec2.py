import boto3
import math

ec2_client = boto3.client("ec2")

root_volume = [ "/dev/sda1", "/dev/xvda" ]

def describe_volumes(instance_id):
    attached_volumes_info = ec2_client.describe_volumes(
        Filters = [
                {
                    "Name": "attachment.instance-id",
                    "Values": [
                        f"{instance_id}",
                    ]
                },
            ]
        )
    # root volume이 아닌 data volume 찾기
    data_volume = None
    for volumes in range(len(attached_volumes_info["Volumes"])):
        attachments = attached_volumes_info["Volumes"][volumes]["Attachments"]
        if attachments:
            if attachments[0]["Device"] not in root_volume:
                data_volume = attachments[0]["Device"]
    if data_volume is None:
        return None, None
            
    attached_data_volume_info = ec2_client.describe_volumes(
        Filters = [
                {
                    "Name": "attachment.instance-id",
                    "Values": [
                        f"{instance_id}",
                    ]
                },
                {
                    "Name": "attachment.device",
                    "Values": [
                        f"{data_volume}",
                    ]
                }
            ]
        )
    
    volume_id = attached_data_volume_info["Volumes"][0]["Attachments"][0]["VolumeId"]
    
    original_volume_size = attached_data_volume_info["Volumes"][0]["Size"]
    
    return volume_id, original_volume_size
        

def modify_volume(volume_id, original_volume_size):
    resized_volume_size = math.ceil(original_volume_size * 1.05)
    
    response = ec2_client.modify_volume(
        VolumeId = f"{volume_id}",
        Size = resized_volume_size,
    )
    
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    
    return resized_volume_size, status_code

def describe_instance(instance_id):
    response = ec2_client.describe_instances(
         Filters = [
                {
                    "Name": "instance-id",
                    "Values": [
                        f"{instance_id}",
                    ]
                },
            ]
        )
    
    tags = response["Reservations"][0]["Instances"][0]["Tags"]
    
    for tag in tags:
        if tag["Key"] == "Name":
            instance_name = tag["Value"]
            return instance_name
        else:
            return None
