import phonenumbers
import pyfiglet
from phonenumbers import carrier, geocoder, timezone
import requests
from bs4 import BeautifulSoup
import json
import argparse
import time
from concurrent.futures import ThreadPoolExecutor
import re
import csv
import yaml
import xml.etree.ElementTree as ET
from tqdm import tqdm
import random
from fake_useragent import UserAgent
import logging
from dataclasses import dataclass, asdict
import validators
from typing import List, Dict, Any
import os
from urllib.parse import quote
import urllib3
urllib3.disable_warnings()

@dataclass
class PhoneNumberResult:
    """Структура для хранения результатов поиска"""
    phone_number: str
    basic_info: Dict
    social_networks: Dict
    messaging_apps: Dict
    professional_networks: Dict
    leak_databases: Dict
    public_records: Dict
    business_directories: Dict
    tech_resources: Dict
    dark_web_results: Dict
    classifieds: Dict
    forums: Dict
    search_engines: Dict
    job_sites: Dict
    archives: Dict
    documents: Dict
    local_directories: Dict
    review_sites: Dict
    government_records: Dict

class PhoneNumberIntel:
    def __init__(self):
        self.headers = {
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.timeout = 10
        self.session = requests.Session()
        self.session.verify = False
        self.retry_count = 3
        self.retry_delay = 2

    def parse_phone(self, phone_number: str) -> Dict:
        """Базовый анализ номера"""
        try:
            parsed_number = phonenumbers.parse(phone_number)
            return {
                "valid": phonenumbers.is_valid_number(parsed_number),
                "formatted": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "country": geocoder.description_for_number(parsed_number, "en"),
                "carrier": carrier.name_for_number(parsed_number, "en"),
                "timezone": timezone.time_zones_for_number(parsed_number),
                "type": str(phonenumbers.number_type(parsed_number)),
                "region": phonenumbers.region_code_for_number(parsed_number),
                "possible": phonenumbers.is_possible_number(parsed_number),
                "national_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country_code": phonenumbers.region_code_for_number(parsed_number),
                "international": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "e164": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            }
        except Exception as e:
            return {"error": str(e)}

    def _make_request(self, url: str) -> Dict:
        """Безопасный запрос к URL с повторными попытками"""
        for attempt in range(self.retry_count):
            try:
                response = self.session.get(
                    url,
                    headers={**self.headers, 'User-Agent': UserAgent().random},
                    timeout=self.timeout
                )
                return {
                    "status": response.status_code,
                    "url": url,
                    "found": response.status_code == 200
                }
            except requests.RequestException:
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
                continue
        return {"status": 0, "url": url, "found": False}

    def search_social_networks(self, phone_number: str) -> Dict:
        """Поиск по социальным сетям"""
        social_networks = {
            "Facebook": f"https://www.facebook.com/search/top/?q={phone_number}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={phone_number}",
            "Twitter": f"https://twitter.com/search?q={phone_number}",
            "Instagram": f"https://www.instagram.com/explore/tags/{phone_number}",
            "VKontakte": f"https://vk.com/search?c[q]={phone_number}&c[section]=people",
            "Odnoklassniki": f"https://ok.ru/search?st.query={phone_number}",
            "Pinterest": f"https://www.pinterest.com/search/pins/?q={phone_number}",
            "TikTok": f"https://www.tiktok.com/search?q={phone_number}",
            "YouTube": f"https://www.youtube.com/results?search_query={phone_number}",
            "Reddit": f"https://www.reddit.com/search/?q={phone_number}",
            "Tumblr": f"https://www.tumblr.com/search/{phone_number}",
            "Flickr": f"https://www.flickr.com/search/?text={phone_number}",
            "MySpace": f"https://myspace.com/search?q={phone_number}",
            "Discord": f"https://discord.com/users/{phone_number}",
            "Twitch": f"https://www.twitch.tv/search?term={phone_number}"
        }
        return {name: self._make_request(url) for name, url in social_networks.items()}
    def search_messaging_apps(self, phone_number: str) -> Dict:
        """Поиск по мессенджерам"""
        messaging_apps = {
            "WhatsApp": f"https://wa.me/{phone_number}",
            "Telegram": f"https://t.me/{phone_number}",
            "Viber": f"viber://chat?number={phone_number}",
            "Skype": f"skype:{phone_number}?call",
            "WeChat": f"weixin://dl/chat?{phone_number}",
            "Line": f"line://ti/p/{phone_number}",
            "Signal": f"signal://chat?number={phone_number}",
            "KakaoTalk": f"kakaotalk://profiles/{phone_number}",
            "ICQ": f"https://icq.im/{phone_number}",
            "Snapchat": f"https://www.snapchat.com/add/{phone_number}"
        }
        return {name: self._make_request(url) for name, url in messaging_apps.items()}

    def search_professional_networks(self, phone_number: str) -> Dict:
        """Поиск по профессиональным сетям"""
        professional_networks = {
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={phone_number}",
            "GitHub": f"https://github.com/search?q={phone_number}&type=users",
            "GitLab": f"https://gitlab.com/search?search={phone_number}",
            "BitBucket": f"https://bitbucket.org/search?q={phone_number}",
            "StackOverflow": f"https://stackoverflow.com/search?q={phone_number}",
            "AngelList": f"https://angel.co/search?q={phone_number}",
            "Xing": f"https://www.xing.com/search?q={phone_number}",
            "Behance": f"https://www.behance.net/search?search={phone_number}",
            "Dribbble": f"https://dribbble.com/search/{phone_number}",
            "DeviantArt": f"https://www.deviantart.com/search?q={phone_number}",
            "Medium": f"https://medium.com/search?q={phone_number}",
            "ProductHunt": f"https://www.producthunt.com/search?q={phone_number}",
            "HackerNews": f"https://hn.algolia.com/?q={phone_number}"
        }
        return {name: self._make_request(url) for name, url in professional_networks.items()}

    def search_leak_databases(self, phone_number: str) -> Dict:
        """Поиск по базам утечек"""
        leak_databases = {
            "HaveIBeenPwned": f"https://haveibeenpwned.com/search?q={phone_number}",
            "DeHashed": f"https://dehashed.com/search?query={phone_number}",
            "LeakCheck": f"https://leakcheck.net/search?type=phone&query={phone_number}",
            "SnusBase": f"https://snusbase.com/search?type=phone&term={phone_number}",
            "LeakPeek": f"https://leakpeek.com/search?q={phone_number}",
            "IntelX": f"https://intelx.io/?s={phone_number}",
            "LeakSite": f"https://leak-lookup.com/search?type=phone&query={phone_number}",
            "BreachDirectory": f"https://breachdirectory.org/{phone_number}",
            "WikiLeaks": f"https://search.wikileaks.org/?q={phone_number}",
            "DataBreaches": f"https://www.databreaches.net/?s={phone_number}"
        }
        return {name: self._make_request(url) for name, url in leak_databases.items()}

    def search_public_records(self, phone_number: str) -> Dict:
        """Поиск по публичным записям"""
        public_records = {
            "TruePeopleSearch": f"https://www.truepeoplesearch.com/results?phoneno={phone_number}",
            "FastPeopleSearch": f"https://www.fastpeoplesearch.com/{phone_number}",
            "WhitePages": f"https://www.whitepages.com/phone/{phone_number}",
            "411": f"https://www.411.com/phone/{phone_number}",
            "Spokeo": f"https://www.spokeo.com/{phone_number}",
            "PeopleFinder": f"https://www.peoplefinder.com/reverse-phone/{phone_number}",
            "ZabaSearch": f"https://www.zabasearch.com/phone/{phone_number}",
            "AnyWho": f"https://www.anywho.com/phone/{phone_number}",
            "USSearch": f"https://www.ussearch.com/search/phone/{phone_number}",
            "SearchPeopleFree": f"https://www.searchpeoplefree.com/phone-lookup/{phone_number}",
            "PublicRecords": f"https://www.publicrecords.com/phone/{phone_number}"
        }
        return {name: self._make_request(url) for name, url in public_records.items()}

    def search_business_directories(self, phone_number: str) -> Dict:
        """Поиск по бизнес-каталогам"""
        business_directories = {
            "YellowPages": f"https://www.yellowpages.com/search?q={phone_number}",
            "Yelp": f"https://www.yelp.com/search?find_desc={phone_number}",
            "BBB": f"https://www.bbb.org/search?find_text={phone_number}",
            "Manta": f"https://www.manta.com/search?search={phone_number}",
            "ChamberOfCommerce": f"https://www.chamberofcommerce.com/united-states?q={phone_number}",
            "Foursquare": f"https://foursquare.com/explore?q={phone_number}",
            "DnB": f"https://www.dnb.com/business-directory/company-search.html?term={phone_number}",
            "OpenCorporates": f"https://opencorporates.com/search?q={phone_number}",
            "CrunchBase": f"https://www.crunchbase.com/search/organizations?q={phone_number}"
        }
        return {name: self._make_request(url) for name, url in business_directories.items()}

    def search_tech_resources(self, phone_number: str) -> Dict:
        """Поиск по техническим ресурсам"""
        tech_resources = {
            "Shodan": f"https://www.shodan.io/search?query={phone_number}",
            "Censys": f"https://censys.io/ipv4?q={phone_number}",
            "ZoomEye": f"https://www.zoomeye.org/searchResult?q={phone_number}",
            "VirusTotal": f"https://www.virustotal.com/gui/search/{phone_number}",
            "SecurityTrails": f"https://securitytrails.com/list/keyword/{phone_number}",
            "GreyNoise": f"https://viz.greynoise.io/query/?gnql={phone_number}",
            "BinaryEdge": f"https://app.binaryedge.io/services/query/{phone_number}",
            "Pastebin": f"https://pastebin.com/search?q={phone_number}"
        }
        return {name: self._make_request(url) for name, url in tech_resources.items()}
    def search_job_sites(self, phone_number: str) -> Dict:
        """Поиск по сайтам работы"""
        job_sites = {
            "Indeed": f"https://www.indeed.com/jobs?q={phone_number}",
            "Monster": f"https://www.monster.com/jobs/search/?q={phone_number}",
            "CareerBuilder": f"https://www.careerbuilder.com/jobs?keywords={phone_number}",
            "Glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={phone_number}",
            "ZipRecruiter": f"https://www.ziprecruiter.com/candidate/search?search={phone_number}",
            "SimplyHired": f"https://www.simplyhired.com/search?q={phone_number}",
            "Dice": f"https://www.dice.com/jobs?q={phone_number}",
            "HeadHunter": f"https://hh.ru/search/vacancy?text={phone_number}"
        }
        return {name: self._make_request(url) for name, url in job_sites.items()}

    def search_classifieds(self, phone_number: str) -> Dict:
        """Поиск по доскам объявлений"""
        classifieds = {
            "Craigslist": f"https://www.craigslist.org/search/sss?query={phone_number}",
            "eBay": f"https://www.ebay.com/sch/i.html?_nkw={phone_number}",
            "Amazon": f"https://www.amazon.com/s?k={phone_number}",
            "Avito": f"https://www.avito.ru/rossiya?q={phone_number}",
            "Gumtree": f"https://www.gumtree.com/search?q={phone_number}",
            "Kijiji": f"https://www.kijiji.ca/b-all/canada/{phone_number}/k0l0",
            "OLX": f"https://www.olx.com/items/q-{phone_number}"
        }
        return {name: self._make_request(url) for name, url in classifieds.items()}

def save_to_csv(results: dict, filename: str):
    """Сохранение результатов в CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Категория', 'Источник', 'Статус', 'URL'])
        
        # Базовая информация
        writer.writerow(['БАЗОВАЯ ИНФОРМАЦИЯ', '', '', ''])
        basic = results.get('basic_info', {})
        for key, value in basic.items():
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            writer.writerow(['', key, str(value), ''])
        
        # Остальные категории
        categories = {
            'СОЦИАЛЬНЫЕ СЕТИ': 'social_networks',
            'МЕССЕНДЖЕРЫ': 'messaging_apps',
            'ПРОФЕССИОНАЛЬНЫЕ СЕТИ': 'professional_networks',
            'БАЗЫ УТЕЧЕК': 'leak_databases',
            'ПУБЛИЧНЫЕ ЗАПИСИ': 'public_records',
            'БИЗНЕС-ДИРЕКТОРИИ': 'business_directories',
            'ТЕХНИЧЕСКИЕ РЕСУРСЫ': 'tech_resources',
            'САЙТЫ РАБОТЫ': 'job_sites',
            'ДОСКИ ОБЪЯВЛЕНИЙ': 'classifieds'
        }
        
        for category_name, category_key in categories.items():
            writer.writerow([category_name, '', '', ''])
            category_data = results.get(category_key, {})
            for source, data in category_data.items():
                status = '✅ Найдено' if data.get('status') == 200 else '❌ Не найдено'
                writer.writerow(['', source, status, data.get('url', '')])

def main():
    parser = argparse.ArgumentParser(description='Advanced Phone Number OSINT Tool')
    parser.add_argument('phone', help='Phone number with country code (e.g. +1234567890)')
    parser.add_argument('--output', help='Output file path', default='results.csv')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('--retry', type=int, default=3, help='Number of retry attempts')
    args = parser.parse_args()

    intel = PhoneNumberIntel()
    intel.timeout = args.timeout
    intel.retry_count = args.retry
    
    banner = pyfiglet.figlet_format("dildosint", font="bloody")
    print(banner)
    print("\n" + "="*60)
    print(f"🔍 Начинаю поиск информации для номера: {args.phone}")
    print("="*60 + "\n")

    results = {}
    
    try:
        with tqdm(total=10, desc="Сбор данных", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            # Базовая информация
            results['basic_info'] = intel.parse_phone(args.phone)
            pbar.update(1)

            # Параллельный поиск
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    'social_networks': executor.submit(intel.search_social_networks, args.phone),
                    'messaging_apps': executor.submit(intel.search_messaging_apps, args.phone),
                    'professional_networks': executor.submit(intel.search_professional_networks, args.phone),
                    'leak_databases': executor.submit(intel.search_leak_databases, args.phone),
                    'public_records': executor.submit(intel.search_public_records, args.phone),
                    'business_directories': executor.submit(intel.search_business_directories, args.phone),
                    'tech_resources': executor.submit(intel.search_tech_resources, args.phone),
                    'job_sites': executor.submit(intel.search_job_sites, args.phone),
                    'classifieds': executor.submit(intel.search_classifieds, args.phone)
                }

                for category, future in futures.items():
                    try:
                        results[category] = future.result()
                        pbar.update(1)
                    except Exception as e:
                        results[category] = {"error": str(e)}
                        pbar.update(1)

        # Сохранение в CSV
        save_to_csv(results, args.output)
        print(f"\n💾 Результаты сохранены в файл: {args.output}")

        # Вывод статистики
        total_sources = sum(1 for cat in results.values() if isinstance(cat, dict) 
                          for data in cat.values() if isinstance(data, dict) and data.get('status') == 200)
        total_checked = sum(len(cat) for cat in results.values() if isinstance(cat, dict))
        
        print("\n📊 СТАТИСТИКА:")
        print("-"*50)
        print(f"• Всего проверено источников: {total_checked}")
        print(f"• Найдено совпадений: {total_sources}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Поиск прерван пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    finally:
        print("\n" + "="*60)
        print("🏁 ПОИСК ЗАВЕРШЕН")
        print("="*60 + "\n")

if __name__ == "__main__":
    main()