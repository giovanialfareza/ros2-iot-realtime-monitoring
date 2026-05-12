from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'bridge_data'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # TAMBAHKAN BARIS INI AGAR FOLDER LAUNCH TERBACA SAAT DI-BUILD
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nama_maintainer',
    maintainer_email='email@domain.com',
    description='Bridge data IoT ke ROS 2 Websocket',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # TAMBAHKAN BARIS INI AGAR NODE PYTHON BISA DIJALANKAN
            'data_publisher = bridge_data.data_publisher:main'
        ],
    },
)