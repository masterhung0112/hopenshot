#ifndef OPENSHOT_READERBASE_H
#define OPENSHOT_READERBASE_H

#include <tr1/memory>
#include "ChannelLayouts.hpp"
#include "Fraction.hpp"
#include <string>
//#include "Frame.hpp"
//#include "Json.hpp"

using namespace std;

namespace openshot
{

	struct ReaderInfo
	{
		bool has_video;
		bool has_audio;
		bool has_single_image;
		float duration;
		long long file_size;
		int height;
		int width;
		int pixel_format;
		Fraction fps;
		int video_bit_rate;
		Fraction pixel_ratio;
		Fraction display_ratio;
		string vcodec;
		long int video_length;
		int video_stream_index;
		Fraction video_timebase;
		bool interlaced_frame;
		bool top_field_first;
		string acodec;
		int audio_bit_rate;
		int sample_rate;
		int channels;
		ChannelLayout channel_layout;
		int audio_stream_index;
		Fraction audio_timebase;
	};

	class ReaderBase
	{
	protected:
		//CriticalSection getFrameCriticalSection;
		//CriticalSection processingCriticalSection;

		int max_width;
		int max_height;
	public:
		ReaderBase();

		ReaderInfo info;

		virtual void Close() = 0;

		void DisplayInfo();

		//virtual CacheBase *GetCache() = 0;

		//virtual tr1::shared_ptr<Frame> GetFrame(long int number) = 0;

		virtual bool IsOpen() = 0;

		virtual string Name() = 0;
#if 0
		virtual string Json() = 0;
		virtual void SetJson(string value) throw(InvalidJSON) = 0;
		virtual Json::Value JsonValue() = 0;
		virtual void setJsonValue(Json::Value root) = 0;
#endif
		void SetMaxSize(int width, int height) {max_width = width; max_height=height;}

		virtual void Open() = 0;
	};
}

#endif /* OPENSHOT_READERBASE_H */
