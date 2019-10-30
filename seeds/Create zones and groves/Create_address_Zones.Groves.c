#include <stdio.h>
#include <stdlib.h>

int main(){
	int l, c,cont=0 ;

	printf("\nINSERT INTO zones (description, complement) VALUES\n");
	printf("(\'Cemitério São João Batista\',\'Novo\'),\n");
	printf("(\'Cemitério São João Batista\',\'Antigo\'),\n");
	printf("(\'Cruzeiro\',\'\'),\n");
	printf("(\'Ala\',\'1\'),\n");
	printf("(\'Ala\',\'2\'),\n");
	printf("(\'Quadra\',\'A\'),\n");
	printf("(\'Quadra\',\'B\'),\n");
	printf("(\'Quadra\',\'C\'),\n");
	printf("(\'Quadra\',\'D\'),\n");
	printf("(\'Valas\',\'\'),\n");
	printf("(\'Valinha\',\'\'),\n");
	printf("(\'Cemitério Santíssimo Sacramento\',\'1\'),\n");
	printf("(\'Cemitério Santíssimo Sacramento\',\'2\');\n");

	//Região - Cemitério São João Batista novo
	//ruas
	cont++;
	printf("--Cemitério São João Batista Novo");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=59;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Cemitério São João Batista antigo
	//ruas
	cont++;
	printf(";--Cemitério São João Batista Antigo");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=73;l<=118;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - cruzeiro
	//ruas
	cont++;
	printf(";--Região - Cruzeiro");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=119;l<=147;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	for(l=174;l<=193;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - ala 1
	//ruas
	cont++;
	printf(";--Região - Ala 1");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=148;l<=173;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - ala 2
	//ruas
	cont++;
	printf(";--Região - Ala 2");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=148;l<=173;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Quadra A
	//ruas
	cont++;
	printf(";--Região - Quadra A");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=26;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Quadra B
	//ruas
	cont++;
	printf(";--Região - Quadra B");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=26;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Quadra C
	//ruas
	cont++;
	printf(";--Região - Quadra C");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=26;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Quadra D
	//ruas
	cont++;
	printf(";--Região - Quadra D");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=26;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Valas
	//ruas
	cont++;
	printf(";--Região - Valas");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=8;l++){
		//numero
		for(c=1;c<=44;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Valinha
	//ruas
	cont++;
	printf(";--Região - Valinha");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=60;l<=72;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Cemitério Santíssimo Sacramento 1
	//ruas
	cont++;
	printf(";--Região - Cemitério Santíssimo Sacramento 1");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=29;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	//Região - Cemitério Santíssimo Sacramento 2
	//ruas
	cont++;
	printf(";--Região - Cemitério Santíssimo Sacramento 2");
	printf("\nINSERT INTO graves (street, number, zone_id) VALUES\n");
	for(l=1;l<=29;l++){
		//numero
		for(c=1;c<=40;c++){
			printf("(\'%d\',\'%d\',%d),", l, c, cont);
		}printf("\n");
	}
	return 0;
}