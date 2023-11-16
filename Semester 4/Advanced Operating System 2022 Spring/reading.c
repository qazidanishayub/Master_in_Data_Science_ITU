#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    int fd, i;
    int *ptr;
    fd = open("file.txt", O_RDONLY);
    ptr = (int*)mmap(0, 1000, PROT_READ, MAP_SHARED, fd, 0);
    for(i = 1; i <= 1000; i++)
    {
        printf("%d ", *ptr);
        ptr++;
    }
    munmap(ptr, 1000);
    close(fd);
    return 0;
}
