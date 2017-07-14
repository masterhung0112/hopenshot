project(hopenshot C CXX)
cmake_minimum_required(VERSION 3.0)

include_directories(include)

set (LIB_SRC
	src/FFmpegReader.cpp
	src/ReaderBase.cpp
	src/Fraction.cpp
)



add_library(hopenshot ${LIB_SRC})

set (TEST_SRC
	tests/FFmpegReader_test.cpp
)
LINK_DIRECTORIES(${CMAKE_BINARY_DIR})
add_executable(FFmpegReader_test ${TEST_SRC})
target_link_libraries(FFmpegReader_test hopenshot cmocka avutil avcodec avformat)
