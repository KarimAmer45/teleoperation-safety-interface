from glob import glob
from setuptools import setup

package_name = "tsi_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Teleoperation Safety Interface contributors",
    maintainer_email="karimamer456@gmail.com",
    description="Telemetry bridge for the Teleoperation Safety Interface Gazebo simulation.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "telemetry_bridge = tsi_bridge.telemetry_bridge:main",
        ],
    },
)
