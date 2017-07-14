#include "FFmpegReader.hpp"

using namespace openshot;
using namespace std;

FFmpegReader::FFmpegReader(string path) throw(InvalidFile, NoStreamsFound, InvalidCodec)

	: path(path), check_fps(false), is_duration_known(false)
{
	int ret;

	/* Initialize FFmpeg */
	av_register_all();
	avformat_network_init();
	avcodec_register_all();

	Open();
}

void FFmpegReader::Close(void)
{
}

void FFmpegReader::Open(void) throw(InvalidFile, NoStreamsFound, InvalidCodec)
{	
	if (!is_open) {
		pFormatCtx = NULL;

		/* Open an input stream, read the header */
		int ret = avformat_open_input(&this->pFormatCtx, path.c_str(), NULL, NULL);
		if (ret != 0) {
			throw InvalidFile("Fail could not be opened.", path);
		}

		/* Retrieve stream information */
		if (avformat_find_stream_info(pFormatCtx, NULL) < 0)
			throw NoStreamsFound("No Streams found in file.", path);
	
		videoStream = -1;
		audioStream = -1;

		/* Loop through each stream, and identify the video and audio stream
		 * index 
		 **/
		for (unsigned int i = 0; i < pFormatCtx->nb_streams; ++i) {
			// Is this video stream
			if (pFormatCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO && videoStream < 0) {
				videoStream = i;
			}
			if (pFormatCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_AUDIO && audioStream < 0) {
				audioStream = i;
			}
		}
		
		if (videoStream < 0 && audioStream < 0) {
			throw NoStreamsFound("No audio and video stream found in file.", path);
		}

		if (videoStream != -1) {
			info.video_stream_index = videoStream;
			pStream = pFormatCtx->streams[videoStream];
			pCodecParam = pFormatCtx->streams[videoStream]->codecpar;
			
			AVCodec *pCodec = avcodec_find_decoder(pCodecParam->codec_id);
			if (pCodec == NULL) {
				throw InvalidCodec("A valid video codec could not be found for this file.", path);
			}

			pCodecCtx = avcodec_alloc_context3(pCodec);
			if (avcodec_parameters_to_context(pCodecCtx, pCodecParam) != 0) {
				throw InvalidCodec("Fail to copy the data from codec param to video codec context", path);
			}

			//pCodecCtx->thread_count = OPEN_MP_NUM_PROCESSORS;

			// Open video codec
			if (avcodec_open2(pCodecCtx, pCodec, NULL) < 0) {
				throw InvalidCodec("A video codec was found, but could not be opened.", path);	
			}

			UpdateVideoInfo();
		}

		if (audioStream != -1) {
			info.audio_stream_index = audioStream;
			aStream = pFormatCtx->streams[audioStream];
			aCodecParam = aStream->codecpar;

			AVCodec *aCodec = avcodec_find_decoder(aCodecParam->codec_id);
			if (aCodec == NULL) {
				throw InvalidCodec("A valid audio codec could not be found for this file.", path);
			}

			aCodecCtx = avcodec_alloc_context3(aCodec);
			if (avcodec_parameters_to_context(aCodecCtx, aCodecParam) != 0) {
				throw InvalidCodec("Fail to copy the data from codec param to audio codec context", path);
			}

			if (avcodec_open2(aCodecCtx, aCodec, NULL) < 0) {
				throw InvalidCodec("A audio codec was found, but could not be opened.", path);
			}

			UpdateAudioInfo();
		}
#if 0
		info.has_audio = ;
		info.has_single_image = ;

		info.interlaced_frame = ;
		info.top_field_first = ;
		info.acodec = ;
		info.audio_bit_rate = ;
		info.sample_rate = ;
		info.channels = ;
		info.channel_layout = ;
		info.audio_stream_index = ;
		info.audio_timebase = ;
#endif
	}
}

FFmpegReader::~FFmpegReader()
{
	avformat_close_input(&pFormatCtx);
}

void FFmpegReader::UpdateVideoInfo()
{
	info.has_video = true;
	info.file_size = pFormatCtx->pb ? avio_size(pFormatCtx->pb) : -1;
	info.height = pCodecParam->height;
	info.width = pCodecParam->width;
	info.vcodec = pCodecCtx->codec->name;
	info.video_bit_rate = pFormatCtx->bit_rate;

	if (!check_fps) {
		info.fps.num = pStream->avg_frame_rate.num;
		info.fps.den = pStream->avg_frame_rate.den;
	}

	if (pStream->sample_aspect_ratio.num != 0) {
		info.pixel_ratio.num = pStream->sample_aspect_ratio.num;
		info.pixel_ratio.den = pStream->sample_aspect_ratio.den; 
	} else if (pCodecParam->sample_aspect_ratio.num != 0) {
		info.pixel_ratio.num = pCodecParam->sample_aspect_ratio.num; 
		info.pixel_ratio.den = pCodecParam->sample_aspect_ratio.den; 
	} else {
		info.pixel_ratio.num = 1;
		info.pixel_ratio.den = 1;
	}

	info.pixel_format = pCodecParam->format;
	//info.pixel_format = pCodecCtx->pix_fmt;

	Fraction size(info.width * info.pixel_ratio.num, info.height * info.pixel_ratio.den);
	size.Reduce();

	info.display_ratio.num = size.num;
	info.display_ratio.den = size.den;

	info.video_timebase.num = pStream->time_base.num;
	info.video_timebase.den = pStream->time_base.den;

	info.duration = pStream->duration * info.video_timebase.ToDouble();

	if (info.duration <= 0.0f && pFormatCtx->duration >= 0)
		// Use the format's duration
		info.duration = pFormatCtx->duration / AV_TIME_BASE;

	if (info.duration <= 0.0f && info.video_bit_rate > 0 && info.file_size > 0) {
		info.duration = (info.file_size / info.video_bit_rate);
	}

	if (info.duration <= 0.0f) {
		info.duration = -1;
		info.video_length = -1;
		is_duration_known = false;
	} else {
		is_duration_known = true;
		info.video_length = round(info.duration * info.fps.ToDouble());
	}

	if (info.fps.ToFloat() > 120.0f || (info.fps.num == 0 || info.fps.den == 0)) {
		info.fps.num = 24;
		info.fps.den = 1;
		info.video_timebase.num = 1;
		info.video_timebase.den = 24;

		info.video_length = round(info.duration * info.fps.ToDouble());
	}
}

void FFmpegReader::UpdateAudioInfo(void)
{
	info.has_audio = true;
	info.file_size = (pFormatCtx->pb) ? avio_size(pFormatCtx->pb) : -1;
	info.acodec = aCodecCtx->codec->name;
	info.audio_bit_rate = aCodecParam->bit_rate;
	info.sample_rate = aCodecParam->sample_rate;
	info.channels = aCodecParam->channels;
	if (aCodecParam->channel_layout == 0) {
		//aCodecParam->channel_layout = av_get_default_channel_layout(aCodecParam->channels);
	}
	info.channel_layout = (ChannelLayout) aCodecParam->channel_layout;
	info.audio_stream_index = audioStream;
	info.audio_timebase.num = aStream->time_base.num;
	info.audio_timebase.den = aStream->time_base.den;
	
	if (aStream->duration > 0.0f && aStream->duration > info.duration) {
		info.duration = aStream->duration * info.audio_timebase.ToDouble();
	}

	if (info.has_video && info.video_length <= 0) {
		info.video_length = info.duration * info.fps.ToDouble();
	}
	
	if (!info.has_video) {
		info.fps.num = 24;
		info.fps.den = 1;
		info.video_timebase.num = 1;
		info.video_timebase.den = 24;

		info.video_length = round(info.duration * info.fps.ToDouble());
		info.width = 720;
		info.height = 480;

	}
}
