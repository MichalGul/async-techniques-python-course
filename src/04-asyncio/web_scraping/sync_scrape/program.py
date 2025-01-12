import datetime
import aiohttp
import asyncio
import requests
import bs4
from colorama import Fore


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    # resp = requests.get(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            return await resp.text()



def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()




def main():

    # Changed this from the video due to changes in Python 3.10:
    # DeprecationWarning: There is no current event loop, loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_title_range())

    t0 = datetime.datetime.now()
    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec.")

    # Required because of https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    loop.run_until_complete(asyncio.sleep(0.250)) # Close underlying connections
    loop.close()

async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)

    tasks = []
    for n in range(150, 160):
        tasks.append((n, asyncio.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(Fore.WHITE + f"Title fotund: {title}", flush=True)


if __name__ == '__main__':
   main()
