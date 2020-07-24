#include<stdio.h>
#include <stdlib.h>
int main()
{
	int n0,n1,n2,n3,n4,n5;
	char str[4];
	str[3]=10; //换行
	
	FILE *fp=fopen("2-6pl3.txt","w");  
    if(fp==NULL)  
    {  
        return 0;  
    } 
	
	
	for(n0=97;n0<123;n0++)
	{
		str[0]=n0;
		//for(n1=97;n1<123;n1++)
		//{
			str[1]=45;
			for(n2=97;n2<123;n2++)
			{
				str[2]=n2;
				fprintf(fp,"%s", str);
			}
			
		//}
	}
	fclose(fp);	
	return 0;				
}
					