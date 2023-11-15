
#include <stdio.h> 
#include <sys/types.h> 
#include <unistd.h> 
#include <stdlib.h> 
#include <sys/wait.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>

#define MB 1024*1024
#define NUM_PROC 4
#define SIZE 2*MB

void search(char* filename, char* phrase) {
    
    int fd = open(filename, O_RDONLY);
    if(fd == -1) {
        perror("open");
        exit(1);
    }
    
    int i, status; 
    pid_t pid; 
    int block_size = SIZE/NUM_PROC;
    int search_len = strlen(phrase);
    long offset = 0;
    long found_at = -1;
    
    // Start clock
    clock_t t;
    t = clock();

    for(i=0; i<NUM_PROC; i++) {
        pid = fork();
        if(pid == -1) {
            perror("fork");
            exit(1);
        }
        else if(pid == 0) {
            // Child process
            
            char buf[block_size];
            ssize_t read_ret;
            
            // Read block from file
            read_ret = read(fd, buf, block_size);
            if(read_ret == -1) {
                perror("read");
                exit(1);
            }
            else if(read_ret == 0) {
                // End of file
                printf("Reached end of file\n");
                exit(1);
            }
            
            // Perform linear search
            long j;
            for(j=0; j<read_ret-search_len; j++) {
                if(strncmp(buf+j, phrase, search_len) == 0) {
                    found_at = offset + j;
                    break;
                }
            }
            
            // Exit child process
            exit(0);
        }
        
        // Parent process
        
        offset += block_size;
        lseek(fd, offset, SEEK_SET);
    }
    
    // Wait for all child processes to terminate
    for(i=0; i<NUM_PROC; i++) {
        wait(&status);
    }
    
    // Stop clock
    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC;
    printf("Search completed in %f seconds\n", time_taken);
    
    printf("Found at %ld\n", found_at);
    
    close(fd);
}

int main() {
    char* filename = "./2gb";
    char* phrase = "the";
    search(filename, phrase);
    return 0;
}
