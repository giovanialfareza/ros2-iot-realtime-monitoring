from setuptools import setup
from builtin_interfaces.msg import Time
from sensor_msgs.msg import Temperature


package_name = 'data_engineering'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Alfareza Giovani',
    maintainer_email='064002200045@std.trisakti.ac.id',
    description='Data Engineering Layer for IoT ROS2 Pipeline',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = data_engineering.publisher_node:main',
        ],
    },
)

