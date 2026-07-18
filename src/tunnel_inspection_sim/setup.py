import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tunnel_inspection_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'models/tunnel'), glob('models/tunnel/*.*')),
        (os.path.join('share', package_name, 'models/tunnel/cracks'), glob('models/tunnel/cracks/*')),
        (os.path.join('share', package_name, 'models/tunnel/texture'), glob('models/tunnel/texture/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seonyeong Jeong',
    maintainer_email='seonyeong4624@gmail.com',
    description='ROS 2 tunnel inspection simulation with autonomous driving, RGB-D crack detection, size estimation, and risk mapping.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_drive = tunnel_inspection_sim.simple_drive:main',
            'wall_following = tunnel_inspection_sim.wall_following:main',
            'crack_detector = tunnel_inspection_sim.crack_detector:main',
        ],
    },
)
