# Heti Discord értesítő

Minden vasárnap **08:00-kor magyar idő szerint** egy Discord webhookon keresztül `@everyone` üzenetet és képet küld. Nincs szükség saját weboldalra, szerverre vagy bekapcsolt számítógépre.

## Telepítés

1. Hozz létre egy **privát GitHub repositoryt** (például `discord-weekly-notifier`).
2. Töltsd fel a ZIP **tartalmát** a repository gyökerébe, a rejtett `.github/workflows/weekly-discord.yml` mappát is megtartva. A GitHub webes feltöltésénél ellenőrizd, hogy a `.github` mappa valóban felkerült. Alternatíva: GitHub Desktop.
3. Discord: a célcsatorna **Integrációk → Webhookok** menüjében hozz létre egy webhookot, majd másold ki az URL-jét.
4. GitHub: **Settings → Secrets and variables → Actions → New repository secret**. Név: `DISCORD_WEBHOOK_URL`, érték: a webhook teljes URL-je. Soha ne tedd az URL-t a forráskódba!
5. Szerkeszd a `config.json` fájlban a `message` szövegét. Az `@everyone` megjelölést a program automatikusan hozzáadja.
6. A kívánt képet tedd az `assets/` mappába `notification.png` néven. JPG/GIF esetén nevezd át az `image_file` értékét is. A mellékelt kép csak egy helyőrző; cseréld le a sajátodra.
7. Nyisd meg a **Actions → Weekly Discord notification → Run workflow** menüt és indíts tesztet. Ez a kézi futtatás **azonnal küld** üzenetet, ezért `@everyone` értesítést is okozhat.

## Időzítés és korlátok

- Két UTC cron-bejegyzés (06:00 és 07:00) biztosítja a nyári/téli időszámítás támogatását. A futtatáskor ellenőrizzük a budapesti helyi időt.
- **A GitHub Actions nem garantálja a pontos 08:00-s indulást.** Ha a GitHub több mint egy percet késik, a szigorú `08:00` ellenőrzés miatt az értesítés **kimaradhat**. Ez a csomag inkább egyszerű, ingyenes kiindulópont, nem garantált kézbesítés. Megbízhatóbb küldéshez egy dedikált időzítő és idempotens, késést tűrő ellenőrzés ajánlott.
- A GitHub ütemezett workflow-k inaktív nyilvános repositoryban 60 nap után letiltódhatnak; privát repository ajánlott.
- A webhooknak jogosultságra van szüksége az `@everyone` megjelöléshez, a Discord tagok értesítési beállításai pedig befolyásolják a tényleges értesítést.
- Ne oszd meg a webhook URL-t másokkal; ha kiszivárog, töröld és készíts újat.
- Az üzenet legfeljebb 2000 karakter, a kép legfeljebb 8 MB lehet ebben a csomagban.

## Fájlok

- `notify.py`: üzenet és kép elküldése.
- `config.json`: üzenet és képfájlnév.
- `assets/notification.png`: cserélhető kép.
- `.github/workflows/weekly-discord.yml`: időzítés és kézi teszt.
