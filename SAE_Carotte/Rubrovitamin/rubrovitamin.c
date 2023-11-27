#include <io.h>
#include <inttypes.h>
#include <avr/eeprom.h>
#include <avr/pgmspace.h>

void sendbytet0(uint8_t b);
uint8_t recbytet0(void);

#define size_ver 4
const char ver_str[size_ver] PROGMEM = "1.00";

// Déclarations des variables globales
uint8_t cla, ins, p1, p2, p3; // Variables de commande
uint8_t sw1, sw2; // Status word

int taille; // Taille des données introduites
#define MAXI 128
uint8_t data_nom[MAXI]; // Données nom
uint8_t data_prenom[MAXI]; // Données prénom
uint8_t data_birth[MAXI]; // Données date de naissance
uint8_t data_solde[MAXI]; // Données de solde

// Variables pour stockage dans la mémoire EEPROM
#define MAX_PERSO 32
uint8_t ee_taille_nom EEMEM = 0; // Taille du nom dans l'EEPROM
unsigned char ee_nom[MAX_PERSO] EEMEM; // Nom stocké dans l'EEPROM
uint8_t ee_taille_prenom EEMEM = 0; // Taille du prénom dans l'EEPROM
unsigned char ee_prenom[MAX_PERSO] EEMEM; // Prénom stocké dans l'EEPROM
uint8_t ee_taille_birth EEMEM = 0; // Taille de la date de naissance dans l'EEPROM
unsigned char ee_birth[MAX_PERSO] EEMEM; // Date de naissance stockée dans l'EEPROM
#define MAX_SOLDE 8
uint8_t ee_taille_solde EEMEM = 0; // Taille du solde dans l'EEPROM
unsigned char ee_solde[MAX_SOLDE] EEMEM; // Solde stocké dans l'EEPROM

uint16_t solde EEMEM = 0;  // Définit une variable "solde" stockée en mémoire EEPROM, initialisée à 0.


// Procédure pour émettre l'ATR (Answer To Reset)
void atr(uint8_t n, char* hist) {
  sendbytet0(0x3b); // Définition du protocole
  n = 0xF0 + n + 1;
  sendbytet0(n); // Nombre d'octets d'historique
  sendbytet0(0x01); // TA 
  sendbytet0(0x05); // TB
  sendbytet0(0x05); // TC 
  sendbytet0(0x00); // TD protocole t=0
  sendbytet0(0x00); // CAT 

  while(n--) { // Boucle d'envoi des octets d'historique
    sendbytet0(*hist++);
  }
}

// Procédure pour émettre la version stockée en mémoire flash
void version() {
  int i;
  if (p3 != size_ver) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = size_ver; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  for (i = 0; i < p3; i++) { // Émission des données de la version
    sendbytet0(pgm_read_byte(ver_str + i));
  }
  sw1 = 0x90; // Succès
}

// Procédure pour introduire un nom et le stocker en EEPROM
void intro_nom() {
  int i;
  unsigned char data_nom[MAX_PERSO];
  if (p3 > MAX_PERSO) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = MAX_PERSO; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  for (i = 0; i < p3; i++) { // Boucle d'envoi du message
    data_nom[i] = recbytet0();
  }
  eeprom_write_block(data_nom, ee_nom, p3); // Écriture du nom en EEPROM
  eeprom_write_byte(&ee_taille_nom, p3); // Stockage de la taille du nom en EEPROM
  sw1 = 0x90; // Succès
}

// Procédure pour lire le nom depuis l'EEPROM
void lire_nom() {
  int i;
  char buffer[MAX_PERSO];
  uint8_t taille;
  taille = eeprom_read_byte(&ee_taille_nom); // Lecture de la taille du nom en EEPROM
  if (p3 != taille) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = taille; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  eeprom_read_block(buffer, ee_nom, taille); // Lecture du nom depuis l'EEPROM

  for (i = 0; i < p3; i++) { // Envoi du nom
    sendbytet0(buffer[i]);
  }
  sw1 = 0x90; // Succès
}

// Procédure pour introduire un prénom et le stocker en EEPROM
void intro_prenom() {
  int i;
  unsigned char data_prenom[MAX_PERSO];
  if (p3 > MAX_PERSO) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = MAX_PERSO; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  for (i = 0; i < p3; i++) { // Boucle d'envoi du message
    data_prenom[i] = recbytet0();
  }
  eeprom_write_block(data_prenom, ee_prenom, p3); // Écriture du prénom en EEPROM
  eeprom_write_byte(&ee_taille_prenom, p3); // Stockage de la taille du prénom en EEPROM
  sw1 = 0x90; // Succès
}

// Procédure pour lire le prénom depuis l'EEPROM
void lire_prenom() {
  int i;
  char buffer[MAX_PERSO];
  uint8_t taille;
  taille = eeprom_read_byte(&ee_taille_prenom); // Lecture de la taille du prénom en EEPROM
  if (p3 != taille) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = taille; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  eeprom_read_block(buffer, ee_prenom, taille); // Lecture du prénom depuis l'EEPROM

  for (i = 0; i < p3; i++) { // Envoi du prénom
    sendbytet0(buffer[i]);
  }
  sw1 = 0x90; // Succès
}

// Procédure pour introduire la date de naissance et la stocker en EEPROM
void intro_birth() {
  int i;
  unsigned char data_birth[MAX_PERSO];
  if (p3 > MAX_PERSO) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = MAX_PERSO; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  for (i = 0; i < p3; i++) { // Boucle d'envoi du message
    data_birth[i] = recbytet0();
  }
  eeprom_write_block(data_birth, ee_birth, p3); // Écriture de la date de naissance en EEPROM
  eeprom_write_byte(&ee_taille_birth, p3); // Stockage de la taille de la date de naissance en EEPROM
  sw1 = 0x90; // Succès
}

// Procédure pour lire la date de naissance depuis l'EEPROM
void lire_birth() {
  int i;
  char buffer[MAX_PERSO];
  uint8_t taille;
  taille = eeprom_read_byte(&ee_taille_birth); // Lecture de la taille de la date de naissance en EEPROM
  if (p3 != taille) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = taille; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  eeprom_read_block(buffer, ee_birth, taille); // Lecture de la date de naissance depuis l'EEPROM

  for (i = 0; i < p3; i++) { // Envoi de la date de naissance
    sendbytet0(buffer[i]);
  }
  sw1 = 0x90; // Succès
}

// Fonction pour lire le solde depuis l'EEPROM
void LectureSolde() {
  int i;
  char buffer[MAX_SOLDE];
  uint8_t taille;
  taille = eeprom_read_byte(&ee_taille_solde); // Lecture de la taille du solde en EEPROM
  if (p3 != taille) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = taille; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  eeprom_read_block(buffer, ee_solde, taille); // Lecture du solde depuis l'EEPROM

  for (i = 0; i < p3; i++) { // Envoi du solde
    sendbytet0(buffer[i]);
  }
  sw1 = 0x90; // Succès
}

// Procédure pour créditer le solde en stockant les données en EEPROM
void credit() {
  int i;
  unsigned char data_solde[MAX_PERSO];
  if (p3 > MAX_SOLDE) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = MAX_SOLDE; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  for (i = 0; i < p3; i++) { // Boucle d'envoi du message
    data_solde[i] = recbytet0();
  }
  eeprom_write_block(data_solde, ee_solde, p3); // Écriture du solde en EEPROM
  eeprom_write_byte(&ee_taille_solde, p3); // Stockage de la taille du solde en EEPROM
  sw1 = 0x90; // Succès
}

// Procédure pour retirer un montant du solde en EEPROM
void Depenser() {
  if (p3 != 2) {
    sw1 = 0x6c; // Taille incorrecte
    sw2 = 2; // Taille attendue
    return;
  }
  sendbytet0(ins); // Acquittement
  uint16_t retrait = ((uint16_t)recbytet0() << 8) + (uint16_t)recbytet0(); // Lecture du montant
  uint16_t solde_mot = eeprom_read_word(&solde); // Lecture du solde depuis l'EEPROM
  if (solde_mot < retrait) {
    sw1 = 0x61; // Solde insuffisant
    return;
  }
  uint16_t montant = solde_mot - retrait; // Calcul du nouveau solde
  eeprom_write_word(&solde, montant); // Écriture du nouveau solde en EEPROM
  sw1 = 0x90; // Succès
}
int main(void) {
  ACSR = 0x80;
  PORTB = 0xff;
  DDRB = 0xff;
  DDRC = 0xff;
  DDRD = 0;
  PORTC = 0xff;
  PORTD = 0xff;
  ASSR = (1 << EXCLK) + (1 << AS2);
  PRR = 0x87;

// Envoi de l'ATR
  atr(11, "Hello scard");

  taille = 0;
  sw2 = 0;
// Boucle infinie pour le traitement des commandes
  for (;;) {
    cla = recbytet0();
    ins = recbytet0();
    p1 = recbytet0();
    p2 = recbytet0();
    p3 = recbytet0();
    sw2 = 0;
    switch (cla) {
      case 0x81:
        switch (ins) {
          case 0:
            version(4, "1.00");
            break;

          case 1:
            intro_nom();
            break;

          case 2:
            lire_nom();
            break;

          case 3:
            intro_prenom();
            break;

          case 4:
            lire_prenom();
            break;

          case 5:
            intro_birth();
            break;

          case 6:
            lire_birth();
            break;

          default:
            sw1 = 0x6d;
        }
        break;

      case 0x82:
        switch (ins) {
          case 1:
            LectureSolde();
            break;

          case 2:
            credit();
            break;

          case 3:
            Depenser();
            break;

          default:
            sw1 = 0x6d;
        }
        break;

      default:
        sw1 = 0x6e;
    }
    sendbytet0(sw1);
    sendbytet0(sw2);
  }
}
