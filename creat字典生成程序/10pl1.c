#include<stdio.h>
#include <stdlib.h>
int main()
{
	int n0,n1,n2,n3,n4,n5;
	char str[2];
	str[1]=10; //换行
	
	FILE *fp=fopen("10pl1.txt","w");  
    if(fp==NULL)  
    {  
        return 0;  
    } 
	
	
	for(n0=48;n0<58;n0++)
	{
		str[0]=n0;
		fprintf(fp,"%s", str);
	}
	fclose(fp);	
	return 0;				
}
					