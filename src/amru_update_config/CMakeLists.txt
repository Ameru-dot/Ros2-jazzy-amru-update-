cmake_minimum_required(VERSION 3.8)
project(amru_update_config)
find_package(ament_cmake REQUIRED)

# Amru Update parameter folder (places, macros, LLM knowledge) and launch files
install(DIRECTORY param launch DESTINATION share/${PROJECT_NAME})

ament_package()
