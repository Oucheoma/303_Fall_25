#Ucheoma Okoma & MD Shah Alam
#SECTION A
import time
import re
from pathlib import Path
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError


wikipedia.set_lang("en")     # for English results
QUERY = "generative artificial intelligence"
OUTDIR = Path("wiki_refs")   # where .txt files will go
OUTDIR.mkdir(exist_ok=True)

def sanitize_filename(name: str) -> str:
    # cleans/removes characters not allowed on common filesystems
    name = re.sub(r'[\\/*?:"<>|]', " ", name).strip()
    # handleswhitespace too
    name = re.sub(r"\s+", " ", name)
    # keeps name to reasonamle lenght
    return name[:200] if len(name) > 200 else name

def main():
    topics = wikipedia.search(QUERY)
    start = time.perf_counter()

    
    seen = set()
    unique_topics = [t for t in topics if not (t in seen or seen.add(t))]

    for topic in unique_topics:
        try:
            page = wikipedia.page(topic, auto_suggest=False)
            title = page.title
            refs = page.references or []

            safe_title = sanitize_filename(title)
            filepath = OUTDIR / f"{safe_title}.txt"

            with open(filepath, "w", encoding="utf-8") as f:
                for ref in refs:
                    line = str(ref).strip()
                    if line:
                        f.write(line + "\n")

            print(f"Wrote {filepath.name} ({len(refs)} references)")

        except DisambiguationError as e:
            print(f"Skipping '{topic}': disambiguation ({len(e.options)} options).")
        except PageError as e:
            print(f"Skipping '{topic}': page not found ({e}).")
        except Exception as e:
            print(f"Error with topic '{topic}': {e}")

    end = time.perf_counter()
    print(f"Completed in {end - start:.2f} seconds.")

if __name__ == "__main__":
    main()


#SECTION B
import time
import re
from pathlib import Path
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from concurrent.futures import ThreadPoolExecutor


wikipedia.set_lang("en")
QUERY = "generative artificial intelligence"
OUTDIR = Path("wiki_refs_concurrent")
OUTDIR.mkdir(exist_ok=True)

def sanitize_filename(name: str) -> str:
    # clean/remove characters invalid on Windows/macOS/Linux
    name = re.sub(r'[\\/*?:"<>|]', " ", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name[:200] 

def wiki_dl_and_save(topic: str) -> tuple[str, str, int]:
    """
    Retrieves the page for `topic` (auto_suggest=False),
    gets title and references, writes refs to <title>.txt (one per line),
    and returns (title, status, ref_count).
    """
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        refs = page.references or []

        filename = OUTDIR / f"{sanitize_filename(title)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for ref in refs:
                f.write(str(ref).strip() + "\n")

        return (title, "ok", len(refs))

    except DisambiguationError as e:
        return (topic, f"disambiguation ({len(e.options)} options)", 0)
    except PageError as e:
        return (topic, f"page not found ({e})", 0)
    except Exception as e:
        return (topic, f"error: {e}", 0)

def main():
    topics = wikipedia.search(QUERY)

    start = time.perf_counter()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(wiki_dl_and_save, topics))
    end = time.perf_counter()

    for title, status, count in results:
        if status == "ok":
            print(f"Wrote '{title}.txt' ({count} references)")
        else:
            print(f"Skipped '{title}': {status}")

    # 4) printing total time taken
    print(f"Concurrent download completed in {end - start:.2f} seconds.")

if __name__ == "__main__":
    main()
