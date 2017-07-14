#include "ReaderBase.hpp"
#include <iostream>
#include <iomanip>

using namespace openshot;

ReaderBase::ReaderBase() {

}

// Display file information
void ReaderBase::DisplayInfo() {
	cout << fixed << setprecision(2) << boolalpha;
	cout << "----------------------------" << endl;
	cout << "----- File Information -----" << endl;
	cout << "----------------------------" << endl;
	cout << "--> Has Video: " << info.has_video << endl;
	cout << "--> Has Audio: " << info.has_audio << endl;
	cout << "--> Has Single Image: " << info.has_single_image << endl;
	cout << "--> Duration: " << info.duration << " Seconds" << endl;
	cout << "--> File Size: " << double(info.file_size) / 1024 / 1024 << " MB" << endl;
	cout << "----------------------------" << endl;
	cout << "----- Video Attributes -----" << endl;
	cout << "----------------------------" << endl;
	cout << "--> Width: " << info.width << endl;
	cout << "--> Height: " << info.height << endl;
	cout << "--> Pixel Format: " << info.pixel_format << endl;
	cout << "--> Frames Per Second: " << info.fps.ToDouble() << " (" << info.fps.num << "/" << info.fps.den << ")" << endl;
	cout << "--> Video Bit Rate: " << info.video_bit_rate/1000 << " kb/s" << endl;
	cout << "--> Pixel Ratio: " << info.pixel_ratio.ToDouble() << " (" << info.pixel_ratio.num << "/" << info.pixel_ratio.den << ")" << endl;
	cout << "--> Display Aspect Ratio: " << info.display_ratio.ToDouble() << " (" << info.display_ratio.num << "/" << info.display_ratio.den << ")" << endl;
	cout << "--> Video Codec: " << info.vcodec << endl;
	cout << "--> Video Length: " << info.video_length << " Frames" << endl;
	cout << "--> Video Stream Index: " << info.video_stream_index << endl;
	cout << "--> Video Timebase: " << info.video_timebase.ToDouble() << " (" << info.video_timebase.num << "/" << info.video_timebase.den << ")" << endl;
	cout << "--> Interlaced: " << info.interlaced_frame << endl;
	cout << "--> Interlaced: Top Field First: " << info.top_field_first << endl;
	cout << "----------------------------" << endl;
	cout << "----- Audio Attributes -----" << endl;
	cout << "----------------------------" << endl;
	cout << "--> Audio Codec: " << info.acodec << endl;
	cout << "--> Audio Bit Rate: " << info.audio_bit_rate/1000 << " kb/s" << endl;
	cout << "--> Sample Rate: " << info.sample_rate << " Hz" << endl;
	cout << "--> # of Channels: " << info.channels << endl;
	cout << "--> Channel Layout: " << info.channel_layout << endl;
	cout << "--> Audio Stream Index: " << info.audio_stream_index << endl;
	cout << "--> Audio Timebase: " << info.audio_timebase.ToDouble() << " (" << info.audio_timebase.num << "/" << info.audio_timebase.den << ")" << endl;
	cout << "----------------------------" << endl;
}


