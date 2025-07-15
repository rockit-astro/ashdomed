cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()

# ====================================================================================

set(PICO_BOARD pico_w CACHE STRING "Board type")
include(pico_sdk_import.cmake)
project(dome_pico C CXX ASM)
project(tcs_pico C CXX ASM)

pico_sdk_init()

add_executable(dome_pico dome_pico.c)
pico_set_program_name(dome_pico "TMO Dome Heartbeat (Dome)")
pico_set_program_version(dome_pico "1.0")
pico_enable_stdio_uart(dome_pico 0)
pico_enable_stdio_usb(dome_pico 1)
target_include_directories(dome_pico PRIVATE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(dome_pico pico_stdlib pico_btstack_classic pico_btstack_cyw43 pico_cyw43_arch_none)
pico_add_extra_outputs(dome_pico)

add_executable(tcs_pico tcs_pico.c)
pico_set_program_name(tcs_pico "TMO Dome Heartbeat (TCS)")
pico_set_program_version(tcs_pico "1.0")
pico_enable_stdio_uart(tcs_pico 0)
pico_enable_stdio_usb(tcs_pico 1)
target_include_directories(tcs_pico PRIVATE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(tcs_pico pico_stdlib pico_btstack_classic pico_btstack_cyw43 pico_cyw43_arch_none)
pico_add_extra_outputs(tcs_pico)