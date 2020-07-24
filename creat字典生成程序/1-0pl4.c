#include<stdio.h>
#include <stdlib.h>
int main()
{
	int n0,n1,n2,n3,n4,n5;
	char str[5];
	str[4]=10; //换行
	
	FILE *fp=fopen("1-0pl4.txt","w");  
    if(fp==NULL)  
    {  
        return 0;  
    } 
	
	
	for(n0=48;n0<58;n0++)
	{
		str[0]=n0;
		//for(n1=48;n1<58;n1++)
		//{
			str[1]=45;
			for(n2=48;n2<58;n2++)
			{
				str[2]=n2;
				for(n3=48;n3<58;n3++)
				{
					str[3]=n3;
					fprintf(fp,"%s", str);
				}
			}
			
		//}
	}
	for(n0=48;n0<58;n0++)
	{
		str[0]=n0;
		for(n1=48;n1<58;n1++)
		{
			str[1]=n1;
			//for(n2=48;n2<58;n2++)
			//{
				str[2]=45;
				for(n3=48;n3<58;n3++)
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
					