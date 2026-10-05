#include <stdbool.h>
#include <stdatomic.h>
#ifdef __EMSCRIPTEN__
#include <emscripten.h>
#else
#define EMSCRIPTEN_KEEPALIVE
#endif
struct retro_game_info;
static _Atomic int result;
extern bool __real_retro_load_game(const struct retro_game_info *);
bool __wrap_retro_load_game(const struct retro_game_info *game) {
    bool accepted = __real_retro_load_game(game);
    atomic_store(&result, accepted ? 1 : -1);
    return accepted;
}
EMSCRIPTEN_KEEPALIVE int retrom_content_load_result(void) { return atomic_load(&result); }
