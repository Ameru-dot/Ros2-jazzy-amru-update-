from glob import glob
from setuptools import find_packages, setup

setup(
    name='amru_update_extension',
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/amru_update_extension/launch', glob('launch/*.py')),
        ('share/ament_index/resource_index/packages', ['resource/amru_update_extension']),
        ('share/amru_update_extension', ['package.xml']),
        ('share/amru_update_extension/config', glob('config/*.yaml')),
        ('share/amru_update_extension/audio', glob('audio/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Amru',
    maintainer_email='amruafif0306@gmail.com',
    description='Amru Update BT nodes: PlayAudio (pre-recorded Malay, Mandarin, Urdu clips)',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'amru_update_extension_node = amru_update_extension.amru_update_extension_node:main',
        ],
    },
)
