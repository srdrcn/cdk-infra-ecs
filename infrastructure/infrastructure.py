from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_ecs_patterns as ecs_patterns,
)
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationProtocol
from aws_cdk.aws_ecr_assets import DockerImageAsset


class SampleTwoServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        vpc = ec2.Vpc(self, "SampleVPC", max_azs=2)  # default is all AZs in region
        cluster = ecs.Cluster(self, "ServiceCluster", vpc=vpc)
        cluster.add_default_cloud_map_namespace(name="service.local")



        frontend_asset = DockerImageAsset(
            self, "frontend", directory="./frontend", file="Dockerfile"
        )
        frontend_task = ecs.FargateTaskDefinition(
            self, "frontend-task", cpu=512, memory_limit_mib=1024,
        )
        frontend_task.add_container(
            "frontend",
            image=ecs.ContainerImage.from_docker_image_asset(frontend_asset),
            essential=True,
            environment={"LOCALDOMAIN": "service.local"},
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="FrontendContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        ).add_port_mappings(ecs.PortMapping(container_port=3080, host_port=3080))


        frontend_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            id="frontend-service",
            service_name="frontend",
            cluster=cluster,  # Required
            cloud_map_options=ecs.CloudMapOptions(name="frontend"),
            cpu=512,  # Default is 256
            desired_count=1,  # Default is 1
            task_definition=frontend_task,
            memory_limit_mib=512,  # Default is 512
            listener_port=80,
            public_load_balancer=True,
        )

        frontend_service.service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(3080), "flask inbound"
        )
