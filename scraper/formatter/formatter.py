import html

from scraper.chapter import Chapter


class Formatter:
    @staticmethod
    def format(chapter: Chapter) -> str:
        return f"""
        <DOCTYPE html>
        <html lang="en">
            <head>
                <title>{chapter.title}</title>
                <meta name="author" content="{chapter.author}"></meta>
            </head>
            <body>
                <h3>{chapter.title}</h3>
                <div align="left">
                {html.escape(chapter.body)}
                </div>
            </body>
        </html>
        """
