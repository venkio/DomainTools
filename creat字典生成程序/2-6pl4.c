#include<stdio.h>
#include <stdlib.h>
int main()
{
	int n0,n1,n2,n3,n4,n5;
	char str[5];
	str[4]=10; //换行
	
	FILE *fp=fopen("2-6pl4.txt","w");  
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
				for(n3=97;n3<123;n3++)
				{
					str[3]=n3;
					fprintf(fp,"%s", str);
				}
			}
			
		//}
	}
	for(n0=97;n0<123;n0++)
	{
		str[0]=n0;
		for(n1=97;n1<123;n1++)
		{
			str[1]=n1;
			//for(n2=97;n2<123;n2++)
			//{
				str[2]=45;
				for(n3=97;n3<123;n3++)
				{
					str[3]=n3;
					fprintf(fp,"%s", str);
				}
			//}
			
		}
	}
	fclose(fp);	
	return 0;				
}