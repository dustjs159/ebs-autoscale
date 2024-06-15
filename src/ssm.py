import boto3
import time

ssm_client = boto3.client("ssm")

def run_command(instance_id):
    shell_script = """
    #!/bin/bash

    MOUNTPOINT="/data"

    MOUNTPOINT_CEHCK=$(lsblk -o NAME,TYPE,MOUNTPOINTS -n | grep $MOUNTPOINT)

    if [ $? -eq 0 ]; then
            echo "Mountpoint Exists"
            DEVICE_CHECK=$(df -Th | grep $MOUNTPOINT | awk '{print $1}' | grep "p")
            if [ ! -z $DEVICE_CHECK ]; then
                    echo "Partition Exists"
                    DEVICE=$(df -Th | grep $MOUNTPOINT | awk '{print $1}' | cut -d 'p' -f 1)
                    PARTITION_NUMBER=$(df -Th | grep $MOUNTPOINT | awk '{print $1}' | cut -d 'p' -f 2)
                    PARTITION=$(df -Th | grep $MOUNTPOINT | awk '{print $1}')
                    echo "Device : $DEVICE, Partition : $PARTITION, Partition Number : $PARTITION_NUMBER"
                    growpart $DEVICE $PARTITION_NUMBER && resize2fs $PARTITION
                    echo $?
            elif [ -z $DEVICE_CHECK ]; then
                    echo "Partition Non Exists"
                    DEVICE=$(df -Th | grep $MOUNTPOINT | awk '{print $1}')
                    PARTITION_NUMBER=$(df -Th | grep $MOUNTPOINT | awk '{print $1}' | cut -d 'p' -f 2)
                    PARTITION=$(df -Th | grep $MOUNTPOINT | awk '{print $1}')
                    echo "Device : $DEVICE"
                    resize2fs $DEVICE
                    echo $?
            fi
    else
            echo "MOUNTPOINT Not Exists"
            exit 1
    fi
    """
    response = ssm_client.send_command(
        InstanceIds = [
            f"{instance_id}"
        ],
        DocumentName = "AWS-RunShellScript",
        Parameters = {
            "commands": [
                f"{shell_script}"
            ]
        },
        CloudWatchOutputConfig = {
            "CloudWatchOutputEnabled": True
        }
    )
    
    command_id = response["Command"]["CommandId"]
    
    return command_id

def command_status_check(instance_id, command_id):
    
    while True:
        response = ssm_client.list_commands(
            CommandId = command_id,
            InstanceId = instance_id
        )
        
        command_status = response["Commands"][0]["Status"]
        
        if command_status in [ "Success", "Failed" ]:
            break
        
        time.sleep(5)
    
    return command_status
