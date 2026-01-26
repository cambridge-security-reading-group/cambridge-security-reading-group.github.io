import datetime
import os
import time
from typing import List, Dict, Optional, Generator, NamedTuple

import jinja2


class Term(NamedTuple):
    title: str
    papers: List['Paper']


class Badge(NamedTuple):
    text: str
    color: str


class Paper(NamedTuple):
    date: str
    title: str
    url: Optional[str]
    citation: Optional[str]
    badge: Optional[Badge]
    is_skipped: bool


# Map repository names to Badge objects
Repositories: Dict[str, Badge] = {
    "USENIX Security": Badge("USENIX Sec", "#ca6510"),
    "Computer and Communications Security": Badge("ACM CCS", "#0a58ca"),
    "Symposium on Security and Privacy": Badge("IEEE S&P", "#6f42c1"),
    "NDSS": Badge("NDSS", "#0a58ca"),
    "Privacy Enhancing Technologies": Badge("PETS", "#1aa179"),
    "arXiv": Badge("arxiv", "#6c757d"),
    "Cryptology ePrint": Badge("iacr", "#6c757d"),
    "Symposium on Operating Systems Design and Implementation": Badge("OSDI", "#fdb721"),
}


def parse_date(date_str: str) -> datetime.datetime:
    """Parse the date string (Wed, DD MMM YY) into a datetime object."""
    try:
        return datetime.datetime.strptime(date_str, '%a, %d %b %y')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format: 'Wed, 01 Jan 20'.")


def format_date(date: datetime.datetime) -> str:
    """Formats a datetime object into a string following the format 'DDth MMM YYYY'."""
    day = date.day
    suffix = 'th' if 4 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f"{day}{suffix} {date.strftime('%b %Y')}"


def parse_paper(lines: List[str]) -> Paper:
    date = format_date(parse_date(lines[0].strip()))
    title = lines[1].strip()
    if title == 'skipped':
        return Paper(date, title, None, None, None, True)

    link = lines[2].strip() if len(lines) > 2 else None
    citation = lines[3].strip() if len(lines) > 3 else None

    # Add badge if known repository in citation
    badge = None
    for repo, badge_obj in Repositories.items():
        if citation and repo in citation:
            badge = badge_obj
    return Paper(date, title, link, citation, badge, False)


def read_paper_file(path: str) -> Term:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip()
        parts = lines.split('\n\n')

    term_title = parts[0].strip()
    papers = [
                 parse_paper(part.split('\n'))
                 for part in parts[1:]
                 if part.strip()
             ][::-1]  # Reverse the order for latest first

    return Term(term_title, papers)


def read_all_paper_files() -> Generator[Term, None, None]:
    input_dir = 'input'
    for filename in sorted(os.listdir(input_dir), reverse=True):
        if filename.endswith('.papers'):
            file_path = os.path.join(input_dir, filename)
            yield read_paper_file(file_path)


def main() -> None:
    start_time = time.time()

    # Load all paper files
    data: List[Term] = list(read_all_paper_files())
    total_terms = len(data)
    total_papers = sum(len([x for x in term.papers if not x.is_skipped]) for term in data)
    print(f"[ ] Total terms: {total_terms}, Total papers: {total_papers}")

    # Set up Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('.'),
        autoescape=jinja2.select_autoescape(),
    )
    template = env.get_template('template.html')

    # Ensure the _dist folder exists and render into index.html
    output_dir = 'dist'
    os.makedirs(output_dir, exist_ok=True)

    last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = template.render(
        terms=data,
        last_updated=last_updated,
        total_papers=total_papers,
    )

    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[ ] Rendered HTML to {output_path}")

    runtime = 1000.0 * (time.time() - start_time)
    print(f"[+] Finished in {runtime:.1f}ms.")


if __name__ == "__main__":
    main()
