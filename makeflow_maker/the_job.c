#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>

void print_help(){
	fprintf(stdout,"Usage: the_job [options]\n");
	fprintf(stdout," %-30s Specifies the unique input file which will be read.\n","-i,--unique-input");
	fprintf(stdout," %-30s Specifies the common input file which will be read.\n","-c,--common-input");
	fprintf(stdout," %-30s Specifies the number of seconds to run. This is independent of reading or writing files\n","-s,--seconds");
	fprintf(stdout," %-30s Specifies the name of the output file. If an input file(s) is specified, the file(s) is(are) copied out. Otherwise 4MB of random data will be written out.\n","-o,--output");
	fprintf(stdout," %-30s Specifies that no output will be written. The file may still be created, if an doutput file name is passed in.\n","-z,--zero-output");
	fprintf(stdout," %-30s Prints out this message\n","-h,--help");
}

void compute_time(unsigned long seconds){
	unsigned long start = (unsigned long)time(NULL);
	unsigned long end;
	int i=0;
	do{
		i+=1;
		end = (unsigned long)time(NULL);
	}while(end-start < seconds);
}

void copy_out(char* name, FILE* f, FILE* f2, int zero_output){
	size_t buff = 0;
	char buffer[4096];
	size_t trans=0;
	FILE* out;
	if(name){
		out = fopen(name,"w+");
	}else{
		out = fopen("/dev/null","w");
	}
	if(zero_output == 1){//no output size..
		fclose(out);
		return;
	}
	if(f){
		do{//f
			trans = fread(buffer,sizeof(char),4096,f);
			fwrite(buffer,sizeof(char),trans,out);
		}while(!(trans < 4096));
	}
	if(f2){
		do{//f2
			trans = fread(buffer,sizeof(char),4096,f2);
			fwrite(buffer,sizeof(char),trans,out);
		}while(!(trans<4096));
	}
	if(!f && !f2){
		int i;
		FILE* rand = fopen("/dev/urandom","r");
		for(i=0; i< (1024); i++){
			trans = fread(buffer,sizeof(char),4096,rand);
			fwrite(buffer,sizeof(char),trans,out);
		}
	}
	fclose(out);
}

int main(int argc, char** argv){

	char* output = NULL;
	char* unique_in = NULL;
	char* same_in = NULL;
	int seconds = 0;
	int zero_output = 0;

	//long opt code inspired from wikipedia page on getopt and makeflow main function
	static struct option inputs[]={
		{"unique-input",1,0,'i'},
		{"common-input",1,0,'c'},
		{"seconds",1,0,'s'},
		{"output",1,0,'o'},
		{"help",0,0,'h'},
		{"zero-output",0,0,'z'},
		{NULL,0,NULL,0}
	};
	
	int c;
	while((c=getopt_long(argc,argv,"hi:c:s:o:",inputs,NULL)) != -1){
		switch(c){
			case 'h':
				print_help();
				break;
			case 'i':
				unique_in = strdup(optarg);
				break;
			case 'c':
				same_in = strdup(optarg);
				break;
			case 's':
				seconds = atoi(optarg);
				break;
			case 'o':
				output = strdup(optarg);
				break;
			case 'z':
				zero_output=1;
				break;
			default:
				break;
		}
	}
	
	FILE* uin = unique_in ? fopen(unique_in,"r") : NULL;
	FILE* cin = same_in   ? fopen(same_in,"r") : NULL;
	
	copy_out(output, uin, cin,zero_output);
	
	compute_time(seconds);
		
	return 0;
}
