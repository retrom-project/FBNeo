#include <assert.h>
#include <stdbool.h>
struct retro_game_info;
extern bool __wrap_retro_load_game(const struct retro_game_info *);
extern int retrom_content_load_result(void);
static bool accepted;
bool __real_retro_load_game(const struct retro_game_info *game) { (void)game; return accepted; }
int main(void) {
    assert(retrom_content_load_result() == 0);
    assert(!__wrap_retro_load_game(0));
    assert(retrom_content_load_result() == -1);
    accepted = true;
    assert(__wrap_retro_load_game(0));
    assert(retrom_content_load_result() == 1);
    accepted = false;
    assert(!__wrap_retro_load_game(0));
    assert(retrom_content_load_result() == -1);
}
