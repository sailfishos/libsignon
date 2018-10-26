#include <stdio.h>
#include <string.h>
#include <error.h>
#include <errno.h>
#include <unistd.h>
#include <pwd.h>
#include <sys/stat.h>

#include <stdbool.h>
#include "signond/signond-common.h"

#define PATH_LEN 256
#define PRIVILEGED_USER "privileged"

int main()
{
    char path[PATH_LEN];
    // Get user home dir
    struct passwd *pwd = getpwuid(getuid());
    if (!pwd) {
        error(ENOENT, ENOENT, "User id %d not found", getuid());
    }
    if ((strlen(pwd->pw_dir) + strlen(signonDefaultStoragePath)) > PATH_LEN) {
        error(ENAMETOOLONG, ENAMETOOLONG, "File name too long");
    }
    strcpy(path, pwd->pw_dir);
    // Skip the first ~ char
    strcat(path, &signonDefaultStoragePath[1]);

    // Get privileged user id and group
    pwd = getpwnam(PRIVILEGED_USER);
    if (!pwd) {
        error(ENOENT, ENOENT, "User %s not found", PRIVILEGED_USER);
    }

    // Set permissions
    if (chown(path, pwd->pw_uid, pwd->pw_gid)) {
        perror("chown");
    }
    if (chmod(path, 0770)) {
        perror("chmod");
    }
    return 0;
}
