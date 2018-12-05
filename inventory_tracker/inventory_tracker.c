#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mysql.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>

typedef struct item {
  char* name;
  unsigned int quantity;
  struct item* next;
} item_t;

item_t* items_list;

void print_menu() {
  printf("\n========= Inventory Tracker Menu =========\n");
  printf("1. List current inventory\n");
  printf("2. Add inventory\n");
  printf("3. Delete inventory\n");
  printf("4. Get inventory from database\n");
  printf("5. Commit to database\n");
  printf("6. Exit\n");
  printf("Please make your selection: ");
}

void print_items() {
  item_t* curr = items_list;
  int i = 1;
  printf("========= Current Inventory =========\n");
  if(curr == NULL) {
    printf("None (your inventory is currently empty)\n");
  }

  while(curr != NULL) {
    printf("%d. %s (quantity: %d)\n", i, curr->name, curr->quantity);
    curr = curr->next;
    i++;
  }
}

item_t* new_item(char* name, unsigned int quantity) {
  item_t* ni = (item_t*)malloc(sizeof(struct item));

  ni->name = name;
  ni->quantity = quantity;
  ni->next = NULL;

  return ni;
}

void add_item() {
  char inp[100] = {0};
  char* name = NULL;
  unsigned int quantity = 0;
  item_t* curr = items_list;
  int already_in_list = 0;

  printf("Input item name: ");
  fgets(inp, 100, stdin);
  strtok(inp, "\n");
  printf("Input item quantity: ");
  scanf("%u", &quantity);
  while((getchar()) != '\n');
  printf("Adding item ");
  printf(inp);
  printf(" with quantity ");
  printf("%u\n", quantity);

  while(curr != NULL) {
    if(strcmp(inp, curr->name) == 0) {
      curr->quantity = curr->quantity + quantity;
      already_in_list = 1;
      break;
    }
    curr = curr->next;
  }

  if(!already_in_list) {
    name = (char*)malloc(64);
    strcpy(name, inp);
    item_t* ni = new_item(name, quantity);
    curr = items_list;
    if(items_list == NULL) {
      items_list = ni;
    } else {
      while(curr->next != NULL) {
        curr = curr->next;
      }
      curr->next = ni;
    }
  }
}

void delete_item() {
  char inp[64] = {0};
  unsigned int quantity = 0;
  item_t* curr = items_list;
  int found_in_list = 0;
  printf("Input item you would like to remove: ");
  fgets(inp, 100, stdin);
  strtok(inp, "\n");
  printf("How many of this item would you like to remove: ");
  scanf("%u", &quantity);
  while((getchar()) != '\n');

  while(curr != NULL) {
    if(strcmp(curr->name, inp) == 0) {
      if(quantity >= curr->quantity) {
        curr->quantity = 0;
        free(curr);
      } else {
        curr->quantity = curr->quantity - quantity;
      }
      printf("Updated item %s to quantity %u.\n", curr->name, curr->quantity);
      found_in_list = 1;
      break;
    }
    curr = curr->next;
  }

  if(!found_in_list) {
    printf("Could not find item %s in inventory list. Please try again.\n", inp);
  }
}

void get_inventory_from_db(MYSQL* con) {
  const char* query = "SELECT * FROM Items";
  if(mysql_query(con, query)) {
    printf("Getting current inventory from database failed: %s\n", mysql_error(con));
    return;
  }

  MYSQL_RES* result = mysql_store_result(con);

  MYSQL_ROW row;
  int i = 1;
  while((row = mysql_fetch_row(result))) {
    printf("%d. %s (quantity: %s)\n", i, row[0], row[1]);
    i++;
  }

}

int commit_db(MYSQL* con) {
  item_t* curr = items_list;
  char query_str[1024] = {0};
  while(curr != NULL) {

    sprintf(query_str, "INSERT INTO Items VALUES('%s', %d)", curr->name, curr->quantity);
    if(mysql_query(con, query_str)) {
      printf("Error executing query: %s.\n", query_str);
      return -1;
    }
    memset(query_str, 0, 1024);
    curr = curr->next;
  }
  return 0;
}

int main(int argc, char* argv[]) {
  char inp[8] = {0};
  char database_ip[32] = {0};
  items_list = NULL;
  int fd;
  struct ifreq ifr;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  ifr.ifr_addr.sa_family = AF_INET;
  strncpy(ifr.ifr_name, "eth0", IFNAMSIZ-1);
  ioctl(fd, SIOCGIFADDR, &ifr);
  close(fd);
  sprintf(database_ip, "%s", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));
  int dot_count = 0;
  for(int i = 0; i < 32; i++) {
    if(database_ip[i] == '.') {
      dot_count++;
    }
    if(dot_count == 3) {
      database_ip[i+1] = '7';
      database_ip[i+2] = '\0';
      break;
    }
  }

  MYSQL *con = mysql_init(NULL);
  if(con == NULL) {
    printf("Error setting up database. Exiting.\n");
    return -1;
  }
  if(!mysql_real_connect(con, database_ip, "inventoryuser", "Mdq4LVBl7HRp5fxCcB", "inventory", 0, NULL, 0)) {
    printf("Error setting up database. Exiting.\n");
    return -1;
  }

  // edit made by 1phan and rashmi

   FILE *fp;

   fp = fopen("/tmp/dbIP.txt", "w+");
   fprintf(fp, "%s", database_ip);
   fclose(fp);

  while(1) {
    print_menu();
    fgets(inp, 8, stdin);
    printf("You selected option: %c\n", inp[0]);
    if(inp[0] == '1') {
      print_items();
    } else if(inp[0] == '2') {
      add_item();
    } else if(inp[0] == '3') {
      delete_item();
    } else if(inp[0] == '4') {
      get_inventory_from_db(con);
    } else if(inp[0] == '5') {
      if(commit_db(con)) {
        printf("Errors committing to database. Please check your database connection.\n");
      } else {
        printf("Successfully committed inventory to database. Exiting.\n");
        break;
      }
    } else if(inp[0] == '6') {
      if(items_list != NULL) {
        printf("You have unsaved changes.");
      }
      printf("Are you sure you want to exit? (y/N) ");
      fgets(inp, 8, stdin);
      if(inp[0] == 'y' || inp[0] == 'Y') {
        break;
      }
    } else {
      printf("Invalid selection. Please try again.\n\n");
    }
  }
  
  mysql_close(con);
  return 0; 
}
