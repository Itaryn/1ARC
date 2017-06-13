#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <windows.h>

int main() {
    printf("You are in a FTP program.\n");
    printf("You can enter 'help' if you need to see the command.\n");
    char commande[20] = "";
    char chemin[100] = "./Server/";
    CreateDirectory("./Server", NULL);
    CreateDirectory("./Client", NULL);
    while (1){
    printf("%s>", chemin);
    scanf("%s", &commande);
    if (strcmp(commande, "help") == 0)
    {
        printf("You have few commands :\n");
        printf(" - cd : Move to any folder\n");
        printf(" - get : Take a file from the Server directory\n");
        printf(" - ls : List of the Folders and Files where you are\n");
        printf(" - delete : Delete a file or a folder\n");
        printf(" - mkdir : Create a folder\n");
        printf(" - put : Add a file in the Server directory\n");
        printf(" - status : Show the statues of the Server\n");
        printf(" - quit : Leave the FTP program\n");
    }
    else if (strcmp(commande, "cd") == 0)
    {
        printf("Change the path\n");
        int erreur = 1;
        while(erreur){
        printf("Enter the new path :\n");
        scanf("%s", &chemin);
        if (opendir(chemin) == NULL){
            printf("The path does not exist\n");
        }
        else{erreur = 0;}
        }
    }
    else if (strcmp(commande, "get") == 0)
    {
        printf("Get a file from the Server\n");
        printf("Enter the file name :\n");
        char nomDuFichier[30] = "";
        scanf("%s", &nomDuFichier);
        copie(nomDuFichier, chemin, "./Client/");
    }
    else if (strcmp(commande, "ls") == 0)
    {
        printf("List of the folders and files in the path '%s'\n", chemin);
        struct dirent *lecture;
        DIR *contenu;
        contenu = opendir(chemin);
        while ((lecture = readdir(contenu))) {
            if (strcmp(lecture->d_name, ".") != 0 && strcmp(lecture->d_name, "..") != 0){
                printf("%s\n", lecture->d_name);
            }
        }
        if (contenu == NULL){
            printf("The path does not exit.\n");
        }
        closedir(contenu);
    }
    else if (strcmp(commande, "delete") == 0)
    {
        printf("Delete a folder or a file\n");
        printf("Enter the name of the folder/file you want to delete :\n");
        char nomDuFichier[30] = "";
        scanf("%s", &nomDuFichier);
        suppression(nomDuFichier, chemin);
    }
    else if (strcmp(commande, "mkdir") == 0)
    {
        printf("Create a folder\n");
        printf("Enter the name of the new folder :\n");
        char nomDuDossier[] = "";
        char temp[100] = "";
        strcpy(temp, chemin);
        printf("%s", temp);
        scanf("%s", &nomDuDossier);
        CreateDirectory(strcat(temp, nomDuDossier), NULL);
    }
    else if (strcmp(commande, "put") == 0)
    {
        printf("Put a file in the Server");
        printf("Enter the name of the file :\n");
        char nomDuFichier[30] = "";
        scanf("%s", &nomDuFichier);
        copie(nomDuFichier, chemin, "./Server/");
    }
    else if (strcmp(commande, "status") == 0)
    {
        printf("Statues of the Server :");
    }
    else if (strcmp(commande, "quit") == 0)
    {
        printf("Goodbye.");
        return 0;
    }
    else
    {
        printf("I didn't know the command, try again or enter 'help'\n");
    }
    }
    return 0;
}

void copie(char *nom[], char *depart[], char *arrive[])
{
    FILE* fichier=NULL;
    fichier = fopen(strcat(depart, nom), "r");
    if(fichier!=NULL){
        int c;
        FILE* copie = NULL;
        char cpArrive[100] = "";
        copie = fopen(strcat(strcpy(cpArrive, arrive), nom), "w");
        do{
            c = fgetc(fichier);
            if(c == EOF){
                break;
            }
            fputc(c, copie);
        }
        while(c != EOF);
        fclose(copie);
        fclose(fichier);
    }
    else{
        printf("Le fichier n'existe pas.\n");
    }
}

void suppression(char *nom[], char *path[])
{
    remove(strcat(path, nom));
}
