import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # 获取参数文件路径
    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam.yaml'))

    # 获取 rviz 配置文件路径
    rviz_config_dir = launch.substitutions.LaunchConfiguration(
        'rviz_config_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping.rviz'))

    # Scanmatcher 节点
    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud', '/rslidar_points')],
        output='screen'
    )

    # 静态变换发布节点
    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', '1', 'base_link', 'rslidar']
    )

    # 基于图的 SLAM 节点
    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
    )

    # RViz2 节点
    rviz2 = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        launch.actions.DeclareLaunchArgument(
            'rviz_config_dir',
            default_value=rviz_config_dir,
            description='Full path to rviz config file to load'),
        mapping,
        tf,
        graphbasedslam,
        rviz2
    ])