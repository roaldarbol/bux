<p align="center">
  <img width="460" height="420" src="https://user-images.githubusercontent.com/25629697/180643476-d350597e-812e-4438-9f8b-18169b7d8a37.png">
</p>

# Still in alpha-mode, and not ready for download. It is planned to be released to PyPi during Fall 2022.
# Welcome! 🐞
Bux is a simple GUI for running experiments. It is aimed to fill a gap between recording various data streams asynchronously and the more powerful, complex solutions such as Bonsai and Autopilot. Bux has to primary types of control: Cameras and microcontrollers (currently only Micropython is supported). This allows the user to seamlessly record multiple synchronized video streams along with control of both environmental sensors (e.g. temperature, humidity, light) and actuators (e.g. motors, peltier elements, etc.). Bux ensures that all data as well as metadata is logged by default, making it suitable for a less tech-savvy audience.

Bux is designed with a few key design principles in mind:
- **Simple**. The primary objective of Bux is to make it simple to run experiments. An easy interface with few . Logging of data and metadata is done by default.
- **Flexible**. The implementation of microcontroller control is an asset which sets it apart from other softwares. Writing micropython code does require some coding practice (compatible with python), but allows both simple and complex tasks to be designed. Once they are written, parameters can modified from the GUI. The GUI is cross-platform, and Bux can thus be run on every operating system (MacOS, Windows, Linux, Raspberry Pi OS).
- **Extendable and maintainable**. Although it doesn't affect the end user, I try simplefy the code as much as possible. The codebase separates functionality from GUI allowing for a possible change of GUI (currently `Tkinter`)
