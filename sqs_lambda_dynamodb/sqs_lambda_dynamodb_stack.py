from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_sqs as sqs,
    aws_dynamodb,
    Duration
    # aws_sqs as sqs,
)
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from constructs import Construct

class SqsLambdaDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        queue = sqs.Queue(
             self, "SfnQueue",
             queue_name = "sqs-ima-lambda-source",
            visibility_timeout=Duration.seconds(300),
            receive_message_wait_time=Duration.seconds(20)
        )
        lambda_fn = lambda_.Function(self, "MyFunc",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="dynamodb_writer.handler",
            code=lambda_.Code.from_asset("lambdas"),
            timeout=Duration.minutes(5), 
            function_name="lambda-ima-dynamo-writer"
            )
        event_source = SqsEventSource(queue)

        lambda_fn.add_event_source(event_source)

        # dynamo db 
        dynamo_tb = aws_dynamodb.Table(
            self, "ima_table",
            partition_key=aws_dynamodb.Attribute(
            name="id",
            type=aws_dynamodb.AttributeType.STRING
            )
        )
        lambda_fn.add_environment("TABLE_NAME", dynamo_tb.table_name)
        dynamo_tb.grant_write_data(lambda_fn)
        