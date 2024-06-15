import boto3
import os

sns_client = boto3.client("sns")

def sns_publish(command_status, host, instance_id, original_volume_size, resized_volume_size):
    if command_status == "Success":
        response = sns_client.publish(
            TopicArn = os.environ["SNS_ALERT"],
            Subject = "EBS Volume Auto-Scaling Succeeded.",
            Message = f"""
                EBS Volume 자동 확장 성공했습니다.
                - 블록체인 노드: {host} 
                - 인스턴스 ID: {instance_id}
                - 기존 볼륨 크기: {original_volume_size} GiB
                - 증설 후 볼륨 크기: {resized_volume_size} GiB
                """
        )
    elif command_status == "Failed":
        response = sns_client.publish(
            TopicArn = os.environ["SNS_ALERT"],
            Subject = "EBS Volume Auto-Scaling Failed.",
            Message = f"""
                EBS Volume 자동 확장 실패했습니다.
                - 블록체인 노드: {host}
                - 인스턴스 ID: {instance_id}
                - 현재 크기: {original_volume_size} GiB
                """
        )
    else:
        response = sns_client.publish(
            TopicArn = os.environ["SNS_ALERT"],
            Subject = "EBS Volume Auto-Scaling Abnormal status",
            Message = f"""
                EBS Volume이 자동 확장 결과 상태 이상
                - 블록체인 노드: {host}
                - 인스턴스 ID: {instance_id}
                - Status: {command_status}
                """
        )
        