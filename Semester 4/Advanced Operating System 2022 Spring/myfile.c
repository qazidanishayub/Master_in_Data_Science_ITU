#include <stdio.h>

#include <stdlib.h>



int main()

{

    FILE *fp;

    fp = fopen("file.txt","w");

    fseek(fp, 20, SEEK_SET);

    fputc('\0', fp);

    fclose(fp);

    printf("file.txt created of 20 bytes");

    return 0;

}


