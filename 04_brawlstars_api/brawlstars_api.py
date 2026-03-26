"""
Brawl Stars API Client
Modul pro komunikaci s Brawl Stars API a práci s hráčskými daty.
"""

import requests
import json
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Načtení proměnných prostředí z .env souboru
load_dotenv()

# ========================
# KONFIGURACE - TADY ZMĚŇTE TAGY
# ========================
PLAYER_TAG = "#JRLLR9QU"  # Tag hráče kterého chcete analyzovat
CLUB_TAG = "#2PR8CJG08"    # Tag klubu (volitelné)
# ========================


class BrawlStarsAPI:
    """Třída pro komunikaci s Brawl Stars API"""
    
    # Konstanta pro base URL API
    BASE_URL = "https://api.brawlstars.com/v1"
    
    def __init__(self):
        """
        Inicializace klienta API.
        API token je načten z proměnné prostředí BRAWLSTARS_API_TOKEN.
        """
        self.token = os.getenv('BRAWLSTARS_API_TOKEN')
        if not self.token:
            raise ValueError(
                "Chyba: BRAWLSTARS_API_TOKEN není nastavena! "
                "Vytvoř soubor .env a přidej svůj token."
            )
        
        # Nastavení HTTP headeru s autentifikací
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """
        Pomocná metoda pro vytváření HTTP requestů.
        
        Args:
            endpoint: API endpoint (bez base URL)
        
        Returns:
            Parsed JSON response nebo None v případě chyby
        """
        try:
            url = f"{self.BASE_URL}{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Vyvolá chybu pro status kódy 4xx, 5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Chyba API: {e}")
            return None
    
    def get_player(self, player_tag: str) -> Optional[Dict]:
        """
        Načtení informací o hráči podle jeho tagu.
        
        Args:
            player_tag: Tag hráče (např. "#2P8UU8JJ0")
        
        Returns:
            Slovník s údaji o hráči nebo None v případě chyby
        """
        # Hráčský tag je potřeba URL-enkódovat (# → %23)
        encoded_tag = player_tag.replace('#', '%23')
        endpoint = f"/players/{encoded_tag}"
        return self._make_request(endpoint)
    
    def get_club(self, club_tag: str) -> Optional[Dict]:
        """
        Načtení informací o klubu podle jeho tagu.
        
        Args:
            club_tag: Tag klubu (např. "#2PR8CJG08")
        
        Returns:
            Slovník s údaji o klubu nebo None v případě chyby
        """
        encoded_tag = club_tag.replace('#', '%23')
        endpoint = f"/clubs/{encoded_tag}"
        return self._make_request(endpoint)
    
    def get_club_members(self, club_tag: str) -> Optional[Dict]:
        """
        Načtení seznamu členů klubu.
        
        Args:
            club_tag: Tag klubu
        
        Returns:
            Slovník s informacemi o členech klubu
        """
        encoded_tag = club_tag.replace('#', '%23')
        endpoint = f"/clubs/{encoded_tag}/members"
        return self._make_request(endpoint)
    
    def get_player_battles(self, player_tag: str) -> Optional[Dict]:
        """
        Načtení poslední bitvy hráče.
        
        Args:
            player_tag: Tag hráče
        
        Returns:
            Slovník s informacemi o bitvách
        """
        encoded_tag = player_tag.replace('#', '%23')
        endpoint = f"/players/{encoded_tag}/battlelog"
        return self._make_request(endpoint)
    
    def save_player_data(self, player_tag: str, filename: str = "player_data.json") -> bool:
        """
        Uložení informací o hráči do JSON souboru.
        
        Args:
            player_tag: Tag hráče
            filename: Název výstupního souboru
        
        Returns:
            True pokud se podařilo, False v případě chyby
        """
        player_data = self.get_player(player_tag)
        if player_data:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(player_data, f, indent=2, ensure_ascii=False)
                print(f"Údaje uloženy do {filename}")
                return True
            except IOError as e:
                print(f"Chyba při zápisu souboru: {e}")
                return False
        return False


def main():
    """Hlavní funkce - příklady použití API"""
    try:
        # Vytvoření API klienta
        api = BrawlStarsAPI()
        print("✓ API klient inicializován\n")
        
        # Příklad 1: Načtení informací o hráči
        print("=== Příklad 1: Informace o hráči ===")
        player = api.get_player(PLAYER_TAG)
        if player:
            print(f"Jméno: {player.get('name', 'N/A')}")
            print(f"Trofeje: {player.get('trophies', 'N/A')}")
            print(f"Úroveň exp: {player.get('expLevel', 'N/A')}")
            print(f"Nejvyšší trofeje: {player.get('highestTrophies', 'N/A')}\n")
        
        # Příklad 2: Načtení posledních bitev
        print("=== Příklad 2: Poslední bitvy ===")
        battles = api.get_player_battles(PLAYER_TAG)
        if battles:
            print(f"Počet bitev: {len(battles.get('items', []))}")
            if battles.get('items'):
                # Zobrazení první bitvy
                first_battle = battles['items'][0]
                print(f"Poslední bitva - Čas: {first_battle.get('battleTime', 'N/A')}")
                print(f"Mód: {first_battle.get('battle', {}).get('mode', 'N/A')}\n")
        
        # Příklad 3: Uložení dat
        print("=== Příklad 3: Uložení dat ===")
        api.save_player_data(PLAYER_TAG, "my_player_data.json")
        
    except ValueError as e:
        print(f"Chyba inicializace: {e}")
        print("\nPostup:")
        print("1. Přejdi na: https://developer.brawlstars.com")
        print("2. Vytvoř si nový API token")
        print("3. Zkopíruj tento .env soubor na .env:")
        print("   BRAWLSTARS_API_TOKEN=tvůj_token")


if __name__ == "__main__":
    main()
