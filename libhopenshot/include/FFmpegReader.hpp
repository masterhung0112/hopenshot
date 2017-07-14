#ifndef HOPENSHOT_FFMPEG_READER_HPP
#define HOPENSHOT_FFMPEG_READER_HPP

#include <string>
#include "ReaderBase.hpp"
#include "Exceptions.h"
extern "C" {
#include <libavformat/avformat.h>
}
using namespace std;

namespace openshot
{
	class FFmpegReader : public ReaderBase
	{
	private:
		bool is_open;
		string path;
		int videoStream;
		int audioStream;
		
		bool check_fps;
		bool is_duration_known;

		AVFormatContext *pFormatCtx;
		AVStream *pStream, *aStream;
		AVPacket *packet;
		AVCodecParameters *pCodecParam, *aCodecParam;
		AVCodecContext *pCodecCtx, *aCodecCtx;
		
		void UpdateVideoInfo(void);
		void UpdateAudioInfo(void);
	public:
		//CacheMemory final_cache;
		bool enable_seek;

		FFmpegReader(string path) throw(InvalidFile, NoStreamsFound, InvalidCodec);
		FFmpegReader(string path, bool inspect_reader) throw(InvalidFile, NoStreamsFound, InvalidCodec);
		~FFmpegReader();

		void Close();
		//CacheMemory *GetCache() { return &final_cache; }

		//tr1::shared_ptr<Frame>(long int requested_frame) throw(OutOfBoundsFrame, ReaderClosed, TooManySeeks);
		
		bool IsOpen() { return is_open; };

		/// Return the type name of the class
		string Name() { return "FFmpegReader"; };
#if 0
		/// Get and Set JSON methods
		string Json(); ///< Generate JSON string of this object
		void SetJson(string value) throw(InvalidJSON); ///< Load JSON string into this object
		Json::Value JsonValue(); ///< Generate Json::JsonValue for this object
		void SetJsonValue(Json::Value root) throw(InvalidFile); ///< Load Json::JsonValue into this object
#endif
		/// Open File - which is called by the constructor automatically
		void Open() throw(InvalidFile, NoStreamsFound, InvalidCodec);

	};
}

#endif /*HOPENSHOT_FFMPEG_READER_HPP*/
