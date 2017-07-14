extern "C" {
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <cmocka.h>
}

#include "FFmpegReader.hpp"

using namespace openshot;

static void FFmpegReader_DisplayInfo(void **state) {
    (void) state; /* unused */

	FFmpegReader reader("videos/sample1.mp4");
	reader.DisplayInfo();
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(FFmpegReader_DisplayInfo),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
