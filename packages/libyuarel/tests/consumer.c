/* Downstream acceptance probe, MIT; not an upstream conformance suite. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <yuarel.h>

#define REQUIRE(x) do { if (!(x)) { fprintf(stderr, "failed: %s\n", #x); return EXIT_FAILURE; } } while (0)

int main(void)
{
    char input[] = "https://example.org:8443/alpha//beta?one=1&flag&empty=#frag";
    struct yuarel url;
    char *parts[4];
    struct yuarel_param params[4];
    REQUIRE(yuarel_parse(&url, input) == 0);
    REQUIRE(url.scheme == input && strcmp(url.scheme, "https") == 0);
    REQUIRE(url.host == input + 8 && strcmp(url.host, "example.org") == 0);
    REQUIRE(url.port == 8443 && strcmp(url.path, "alpha//beta") == 0);
    REQUIRE(strcmp(url.query, "one=1&flag&empty=") == 0 && strcmp(url.fragment, "frag") == 0);
    REQUIRE(yuarel_split_path(url.path, parts, 4) == 2);
    REQUIRE(parts[0] == url.path && strcmp(parts[0], "alpha") == 0 && strcmp(parts[1], "beta") == 0);
    REQUIRE(yuarel_parse_query(url.query, '&', params, 4) == 3);
    REQUIRE(params[0].key == url.query && strcmp(params[0].key, "one") == 0 && strcmp(params[0].val, "1") == 0);
    REQUIRE(strcmp(params[1].key, "flag") == 0 && params[1].val == NULL);
    REQUIRE(strcmp(params[2].key, "empty") == 0 && params[2].val != NULL && *params[2].val == '\0');
    {
        char bad[] = "://missing";
        REQUIRE(yuarel_parse(&url, bad) == -1);
        REQUIRE(yuarel_parse(NULL, bad) == -1);
        REQUIRE(yuarel_parse(&url, NULL) == -1);
        REQUIRE(yuarel_parse_query(NULL, '&', params, 4) == -1);
    }
    puts("downstream: all three public APIs and in-place pointers passed");
    return EXIT_SUCCESS;
}
