
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    int fd, i;
    int *ptr;
    fd = open("file.txt", O_RDWR);
    ptr = (int*)mmap(0, 1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    for(i = 1; i <= 1000; i++)
    {
        *ptr = i;
        ptr++;
        printf("%d ", i);
    }
    munmap(ptr, 1000);
    close(fd);
    return 0;
}
